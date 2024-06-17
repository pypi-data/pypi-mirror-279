"""stdfconvert

Usage:
  stdfconvert <inglob> <outdir> <format> [--output-machine-readable] [--wide-format] 

"""

import os
import rich
import rich.progress
import subprocess
from rich.progress import Progress
import glob
import pathlib
import ams_rw_stdf
import collections
from docopt import docopt
import toml
import shutil
from dataclasses import dataclass
import polars as pl
import time
from multiprocessing import Pool
import multiprocessing
import queue
import sys
import pickle
import traceback
import random
from collections.abc import Iterable


_schema = [('Test_Nr', pl.UInt32),
          ('Test_Name', pl.Utf8),
          ('ULim', pl.Float32),
          ('LLim', pl.Float32),
          ('res', pl.Float32),
          ('part_id', pl.Utf8),
          ("X_coord", pl.Int32),
          ("Y_coord", pl.Int32),
          ("part_txt", pl.Utf8),
          ("head", pl.Int32),
          ("site", pl.Int32)]

@dataclass
class convertResult:
    exceptions: int
    starts: int
    donnes: int



def convert_list_of_files(flist, outdir, format="parquet", wideFormat=False, logger=None):
    if not isinstance(flist, str) and isinstance(flist, Iterable):
        rich.print("[bold red]deprecated please do not pass iterable of files, but string which can be passed to glob.iglob\n\n[/bold red] ")
        accu = convertResult(0, 0, 0)
        for item in flist:
            res = convert_list_of_files(item, outdir, format, wideFormat)
            accu.donnes += res.donnes
            accu.starts += res.starts
            accu.exceptions += res.exceptions
        rich.print("[bold red]deprecated please do not pass iterable of files, but string which can be passed to glob.iglob\n\n[/bold red] ")
        return accu
    else:
        with Progress(rich.progress.TimeElapsedColumn(),
                    rich.progress.DownloadColumn(), rich.progress.BarColumn(),
                    rich.progress.TransferSpeedColumn(),
                    rich.progress.TimeRemainingColumn(),
                    rich.progress.TextColumn("[progress.description][red]{task.description}")) as progress:
            outdir = pathlib.Path(outdir).resolve()
            outdir.mkdir(exist_ok=True)
            tasks = {}
            args = [sys.executable, "-m", "ams_rw_stdf.convert", flist, outdir, format, "--output-machine-readable"]
            if wideFormat:
                args += ["--wide-format"]
            exceptions = 0
            starts = 0
            donne = 0
            with subprocess.Popen(args, stdout=subprocess.PIPE) as p:
                while True:
                    try:
                        (fileName, msgType, value) = pickle.load(p.stdout)
                        if msgType == "start":
                            tasks[fileName] = progress.add_task(f"{pathlib.Path(fileName).name}", total=value)
                            starts += 1
                        elif msgType == "progress":
                            progress.update(tasks[fileName], completed=value)
                        elif msgType == "donne":
                            progress.remove_task(tasks[fileName])
                            donne += 1
                            del tasks[fileName]
                        elif msgType == "exception":
                            exceptions += 1 
                            if logger:
                                logger.error(f"""exception while converting file {fileName} "{value}" of type "{type(value)}" """)
                            progress.console.print(value)
                        elif msgType == "info":
                            if logger:
                                logger.info(f"""info while converting file {fileName} "{value}" """)
                            progress.console.print(value)
                        elif msgType == "warning":
                            if logger:
                                logger.warn(f"""warning while converting file {fileName} "{value}" """)
                            progress.console.print("WARN: " + value)
                    except EOFError:
                        break
                    except Exception as e:
                        progress.console.print("terminating:", e, type(e))
                        break
            return convertResult(starts=starts, donnes=donne, exceptions=exceptions)

def _make_new_set_of_params(flist):
    for ifname in flist:
        sys.stdout.buffer.write(pickle.dumps((ifname, "start", os.stat(ifname).st_size)))
        yield ifname

def workFileListAndWriteToStdout(outdir, flist, format, max_running_conversions, unpackCommands, wideFormat, lowEndForRandomDelay=0, highEndForRandomDelay=1000000):
    outdir = pathlib.Path(outdir).resolve()

    with multiprocessing.Manager() as manager, Pool(max_running_conversions) as p:
        progressInfoQueue = manager.Queue()
        tasksToDo = ((ifname, pathlib.Path(outdir/pathlib.Path(ifname).name).with_suffix("." + format), 
                      format, unpackCommands, progressInfoQueue, wideFormat,
                      lowEndForRandomDelay, highEndForRandomDelay)
                      for ifname in _make_new_set_of_params(flist))
        async_res = p.starmap_async(stdf2OutputDirectly, tasksToDo)
        while not async_res.ready():
            try:
                msg = progressInfoQueue.get(timeout=0.001)
                sys.stdout.buffer.write(pickle.dumps(msg))
                sys.stdout.buffer.flush()
            except queue.Empty:
                pass
@dataclass
class part:
    test_num: None
    test_name: None
    hi_lim: None
    lo_lim: None
    res: None

@dataclass
class pin_map_info:
    CHAN_TYP: str
    CHAN_NAM: str
    PHY_NAM: str
    LOG_NAM: str
    HEAD_NUM: int
    SITE_NUM: int

def _worker(iFileName, progressInfoQueue, unpackCommands, lowEndForRandomDelay, highEndForRandomDelay):
    data =  collections.defaultdict(lambda : part([],[],[],[],[]))
    pinDb = {}
    try:
        extension = pathlib.Path(iFileName).suffix
        if extension in {'.stdf', ".std"}:
            iFile = open(iFileName, "rb")
            observeProgress = iFile
        else:
            iFileCompressed = open(iFileName, "rb")
            observeProgress = iFileCompressed
            iFile = subprocess.Popen(unpackCommands[extension], shell=True, stdin=iFileCompressed, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout
        next_output = 0
        accu = {"Test_Nr": [], "Test_Name": [], "ULim": [], "LLim": [], "res": [], "part_id" : [], "X_coord": [], "Y_coord": [], "part_txt" : [], "site" : [], "head" : []}
        for c in ams_rw_stdf.records_no_length_simplified(iFile):
            c = dict(c)
            type_and_subtyp = (c["REC_TYP"], c["REC_SUB"],)
            PL = c["PL"]
            if type_and_subtyp == (15, 10,):
                PL = dict(PL)
                key = (PL["HEAD_NUM"],  PL["SITE_NUM"],)
                p = data[key]
                p.test_num.append(PL["TEST_NUM"])
                p.test_name.append( PL["TEST_TXT"])
                p.hi_lim.append( PL["HI_LIMIT"])
                p.lo_lim.append( PL["LO_LIMIT"])
                p.res.append( PL["RESULT"])
            elif type_and_subtyp == (1, 60,):
                PL = dict(PL)
                pinDb[PL["PMR_INDX"]] = pin_map_info(PL["CHAN_TYP"],
                                                     PL["CHAN_NAM"],
                                                     PL["PHY_NAM"],
                                                     PL["LOG_NAM"],
                                                     PL["HEAD_NUM"],
                                                     PL["SITE_NUM"])
            elif type_and_subtyp == (15, 15,):
                PL = dict(PL)
                key = (PL["HEAD_NUM"],  PL["SITE_NUM"],)
                p = data[key]
                t_num = PL["TEST_NUM"]
                t_txt = PL["TEST_TXT"]
                h_lim = PL["HI_LIMIT"]
                l_lim = PL["LO_LIMIT"]
                for idx, (pmridx, result,) in enumerate(zip(PL["RTN_INDX"], PL["RTN_RSLT"])):
                    p.test_num.append(t_num)
                    try:
                        p.test_name.append(f"{t_txt}/{pinDb[pmridx].PHY_NAM}")
                    except KeyError:
                        progressInfoQueue.put((iFileName, "warning", f"MPR record using PMR idx {pmridx} found but pin undefined!"))
                        p.test_name.append(f"{t_txt}/no_pin_def_for_idx_{pmridx}_running_number_{idx}")
                    p.hi_lim.append(h_lim)
                    p.lo_lim.append(l_lim)
                    p.res.append(result)
            elif type_and_subtyp == (5, 20,):
                PL = dict(PL)
                key = (PL["HEAD_NUM"], PL["SITE_NUM"])
                p = data[key]
                p.test_num.append(None)
                p.test_name.append("SBIN_from_prr_record")
                p.hi_lim.append( None)
                p.lo_lim.append( None)
                p.res.append(PL["SOFT_BIN"])
                numItems = len(p.test_num)
                accu["Test_Nr"].extend(p.test_num)
                accu["Test_Name"].extend(p.test_name)
                accu["ULim"].extend(p.hi_lim)
                accu["LLim"].extend(p.lo_lim)
                accu["res"].extend(p.res)
                accu["part_id"].extend([PL["PART_ID"]]*numItems) 
                accu["X_coord"].extend([PL["X_COORD"]]*numItems)
                accu["Y_coord"].extend([PL["Y_COORD"]]*numItems)
                accu["part_txt"].extend([PL["PART_TXT"]]*numItems)
                accu["site"].extend([PL["SITE_NUM"]]*numItems)
                accu["head"].extend([PL["HEAD_NUM"]]*numItems)
                if (ct:=time.time_ns()) > next_output:
                    progressInfoQueue.put((iFileName, "progress", observeProgress.tell()))
                    next_output = ct+random.randint(lowEndForRandomDelay, highEndForRandomDelay)
                    yield pl.DataFrame(accu, schema=_schema)
                    accu = {"Test_Nr": [], "Test_Name": [], "ULim": [], "LLim": [], "res": [], "part_id" : [], "X_coord": [], "Y_coord": [], "part_txt" : [], "site" : [], "head" : []}
                data[key] = part([],[],[],[],[])
            elif type_and_subtyp == (1, 10,):
                PL = collections.defaultdict(lambda : "NA", dict(PL))
                yield (PL["TEST_COD"], PL["LOT_ID"], PL["OPER_NAM"], PL["START_T"], PL["NODE_NAM"], PL["JOB_NAM"], PL["SBLOT_ID"], PL["FLOOR_ID"], PL["TST_TEMP"])
            elif type_and_subtyp == (1, 20,):
                progressInfoQueue.put((iFileName, "progress", observeProgress.tell()))
                yield pl.DataFrame(accu, schema=_schema)
                return
    except Exception as e:
        progressInfoQueue.put((iFileName, "exception", e))
        return


def stdf2OutputDirectly(iFile, ofile, format, unpackCommands, progressInfoQueue, wideFormat, lowEndForRandomDelay=0, highEndForRandomDelay=100000):
    try:
        w = _worker(iFile, progressInfoQueue, unpackCommands, lowEndForRandomDelay, highEndForRandomDelay)
        (test_cod, lot_id, operator, start_t, node_nam, job_nam, sblot_id, floor_id, tst_temp) = next(w)
        with pl.StringCache():
            if wideFormat:
                def work_df(df):
                    df = df.filter(~pl.col("Test_Name").str.contains(":"))
                    pivot_columns = ["part_id", "site", "head", "X_coord", "Y_coord"] 
                    pivot_columns = [item for item in pivot_columns if item in df.columns]
                    return (df.pivot(index=pivot_columns, values="res", columns=["Test_Name"], aggregate_function="last"))
                df = pl.concat((work_df(item) for item in w), how="diagonal")
                df = df.with_columns(pl.lit(test_cod).cast(pl.Categorical).alias("test_cod"),
                                        pl.lit(lot_id).cast(pl.Categorical).alias("lot_id"),
                                        pl.lit(operator).cast(pl.Categorical).alias("operator"),
                                        pl.lit(start_t).cast(pl.UInt32).alias("START_T"),
                                        pl.lit(tst_temp).cast(pl.Categorical).alias("tst_temp"),
                                        pl.lit(node_nam).cast(pl.Categorical).alias("node_nam"),
                                        pl.lit(job_nam).cast(pl.Categorical).alias("job_nam"),
                                        pl.lit(sblot_id).cast(pl.Categorical).alias("sblot_id"),
                                        pl.lit(floor_id).cast(pl.Categorical).alias("floor_id"),
                                        pl.lit(pathlib.Path(iFile).name).cast(pl.Categorical).alias("filename"))
            else:
                df = pl.concat(w)
                df = df.with_columns(pl.lit(test_cod).cast(pl.Categorical).alias("test_cod"),
                                        pl.lit(lot_id).cast(pl.Categorical).alias("lot_id"),
                                        pl.lit(operator).cast(pl.Categorical).alias("operator"),
                                        pl.lit(start_t).cast(pl.UInt32).alias("START_T"),
                                        pl.lit(tst_temp).cast(pl.Categorical).alias("tst_temp"),
                                        pl.lit(node_nam).cast(pl.Categorical).alias("node_nam"),
                                        pl.lit(job_nam).cast(pl.Categorical).alias("job_nam"),
                                        pl.lit(sblot_id).cast(pl.Categorical).alias("sblot_id"),
                                        pl.lit(floor_id).cast(pl.Categorical).alias("floor_id"),
                                        pl.col("Test_Name").cast(pl.Categorical).alias("Test_Name"),
                                        pl.col("part_id").cast(pl.Categorical).alias("part_id"),
                                        pl.col("part_txt").cast(pl.Categorical).alias("part_txt"))

        if df.is_empty(): # writing out an empty dataframe yields a unreadable parquet file... (https://github.com/pola-rs/polars/issues/13457)
            progressInfoQueue.put((iFile, "exception", f"failed to convert: {iFile}, result is empty..."))
        else:
            if format == "parquet":
                df.write_parquet(ofile)
            elif format in {"ipc", "feather"}:
                df.write_ipc(ofile)
            elif format == "xlsx":
                df.write_excel(ofile)
            
        progressInfoQueue.put((iFile, "donne", None))
    except Exception as e:
        progressInfoQueue.put((iFile, "exception", f"traceback: {''.join(traceback.format_exception(e))}"))
        progressInfoQueue.put((iFile, "exception", f"exception of type {type(e)}: {e}"))

def main():
    options = docopt(__doc__)
    if options["--output-machine-readable"]:
        typical7zLocations = ["7z", "7Z", f"{os.getenv('ProgramFiles(x86)')}/7-Zip/7z.exe", f"{os.getenv('ProgramFiles')}/7-Zip/7z.exe"]
        sevenZLocations = [shutil.which(item) for item in typical7zLocations]
        sevenZLocations = [item for item in sevenZLocations if item is not None]
        if sevenZLocations:
            sevenZ = sevenZLocations[0]
            gzip_handler = f"\"{sevenZ}\" e -tgzip -si -so"
            bzip_handler = f"\"{sevenZ}\" e -tbzip -si -so"
            xz_handler = f"\"{sevenZ}\" e -txz -si -so"
        else:
            gzip_handler         = shutil.which("zcat")
            bzip_handler         = shutil.which("bzcat")
            xz_handler           = shutil.which("unxz")
        
        max_running_conversions = (os.cpu_count()*3)//2
        lowEndForRandomDelay  = 125000000
        highEndForRandomDelay = 400000000
        for configfile in ["/etc/stdf-tamer.toml", pathlib.Path(os.path.expanduser("~")) / ".config/stdf-tamer.toml"]:
            try:
                config = toml.load(configfile)["converter"]
                if "max_running_conversions" in config:
                    max_running_conversions   = config["max_running_conversions"]
                if "zcat" in config:
                    gzip_handler = config["zcat"]
                if "bzcat" in config:
                    bzip_handler = config["bzcat"]
                if "unxz" in config:
                    xz_handler = config["unxz"]
                if "lowEndForRandomDelay" in config:
                    lowEndForRandomDelay = config["lowEndForRandomDelay"]
                if "highEndForRandomDelay" in config:
                    highEndForRandomDelay = config["highEndForRandomDelay"]
            except FileNotFoundError as _:
                pass
            except KeyError as e:
                sys.stdout.buffer.write(pickle.dumps((None, "exception", e)))
            except Exception as e:
                sys.stdout.buffer.write(pickle.dumps((None, "exception", e)))

        try:
            workFileListAndWriteToStdout(options["<outdir>"], glob.iglob(options["<inglob>"]), options["<format>"], max_running_conversions, 
                                         {".gz": gzip_handler, ".xz": xz_handler, ".bz": bzip_handler}, options["--wide-format"], 
                                         lowEndForRandomDelay, highEndForRandomDelay)
        except Exception as e:
            sys.stdout.buffer.write(pickle.dumps((None, "exception", e)))
    else:
        res = convert_list_of_files(options["<inglob>"], options["<outdir>"], options["<format>"], options["--wide-format"])
        sys.stdout.buffer.write(pickle.dumps((None, "info", f"started: {res.starts}, donne: {res.donnes}, exceptions: {res.exceptions}")))


if __name__ == "__main__":
    main()
