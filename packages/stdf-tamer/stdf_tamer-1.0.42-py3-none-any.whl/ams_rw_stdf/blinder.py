"""Blinding stdf file.

This changes test names, numbers, units, scale and limits.
The metadata, timestamps, equipment/operator identifiers etc remains
unchanged.

This is intended to allow to distribute and share STDF files
without the need of an NDA or risking company secrets.

Usage:
  stdfblinder <inglob> <outdir>
  
Options:
  -h --help     Show this screen.
"""
from docopt import docopt
import ams_rw_stdf
import construct.core
import pathlib
import glob
from ams_rw_stdf._opener_collection import _opener
import random
import logging
from rich.logging  import RichHandler
from rich.progress import Progress
from rich.console import Console
import struct
import sys


FORMAT = "%(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])
log = logging.getLogger("rich")
error_console = Console(stderr=True, style="bold red")
        

class endScanning(Exception):
    pass


parser = ams_rw_stdf.compileable_RECORD.compile()


def get_construct_and_bytes(f):
    global parser
    try:
        b = ams_rw_stdf.get_record_bytes(f)
        c = parser.parse(b)
        return (b, c)
    except construct.core.StreamError as e:
        if "stream read less than specified amount, expected 2, found 0" not in str(e):
            log.warning(e)
    except endScanning:
        pass
    except struct.error:
        pass
    except construct.core.ConstError:
        pass
    except EOFError:
        pass
    raise endScanning()
    

def _collect_test_info(state, c, _):
    set_of_tname_tnum_tuples, already_logged = state
    if c.REC_TYP == 15 and (c.REC_SUB == 10 or c.REC_SUB == 20):
        key = (c.PL.TEST_NUM, c.PL.TEST_TXT,)
        if c.PL.LO_LIMIT is not None and c.PL.HI_LIMIT  is not None :
            set_of_tname_tnum_tuples[(c.PL.TEST_NUM, c.PL.TEST_TXT,)] = (c.PL.LO_LIMIT, c.PL.HI_LIMIT,)
        elif key not in set_of_tname_tnum_tuples and key not in already_logged:
            log.warning(f"no hlim/llim entry for {c.PL.TEST_NUM}/{c.PL.TEST_TXT}")
            already_logged = already_logged | {key}
    return (set_of_tname_tnum_tuples, already_logged,)


def generate_result(state, c, b):
    set_of_tname_tnum_tuples, blind_identifier_lookup_table, out_f, already_loged = state
    if c.REC_TYP == 15 and (c.REC_SUB == 10 or c.REC_SUB == 20):
        try:
            llim, hlim = set_of_tname_tnum_tuples[(c.PL.TEST_NUM, c.PL.TEST_TXT,)]
            nTnum, nTname = blind_identifier_lookup_table[(c.PL.TEST_NUM, c.PL.TEST_TXT,)]
            c.PL.UNITS = "[1]"
            if c.PL.RES_SCAL or c.PL.LLM_SCAL or c.PL.HLM_SCAL:
                c.PL.RES_SCAL = 1
                c.PL.LLM_SCAL = 1
                c.PL.HLM_SCAL = 1
            if c.PL.HI_LIMIT or c.PL.LO_LIMIT:
                c.PL.HI_LIMIT = 1
                c.PL.LO_LIMIT = -1
            if hlim == llim:
                hlim = hlim+1
                llim = llim-1
            if hlim-llim > 0:
                c.PL.RESULT = 2.0 * ((c.PL.RESULT- llim)/(hlim-llim)) - 1
                c.PL.TEST_NUM = nTnum
                c.PL.TEST_TXT = nTname
                out_f.write(ams_rw_stdf.RECORD.build(c))
            else:
                if (c.PL.TEST_NUM, c.PL.TEST_TXT,) not in already_loged:
                    log.warning(f"can't transform '{c.PL.TEST_NUM}/{c.PL.TEST_TXT}' as hlim = llim {hlim}/{llim}")
                    already_loged = set(already_loged) | {(c.PL.TEST_NUM, c.PL.TEST_TXT,)}
        except KeyError:
            pass
    else:
        out_f.write(b)
    if c.REC_TYP == 1 and c.REC_SUB == 20:
            raise endScanning()
    return (set_of_tname_tnum_tuples, blind_identifier_lookup_table, out_f, already_loged)


def main():
    arguments = docopt(__doc__)
    inglob = arguments["<inglob>"]
    odir = arguments["<outdir>"]
    if not pathlib.Path(odir).is_dir():
        error_console.print(f"The output directory ({odir}) does not exist!")
        sys.exit(1)

    set_of_tname_tnum_tuples = dict()
    blind_identifier_lookup_table = dict()

    files = list(glob.glob(inglob))
    with Progress() as progress:
        progress_tracker = progress.add_task("[green]scanning stdfs...", total=len(files))
        already_logged = set()
        state = (set_of_tname_tnum_tuples, already_logged,)        
        for si in files:
            si_ftype = pathlib.Path(si).suffix
            with _opener[si_ftype](si, "rb") as f:
                try:
                    while True:
                        b, c = get_construct_and_bytes(f)
                        state = _collect_test_info(state, c, b)
                except endScanning:
                    pass
            progress.update(progress_tracker, advance=1)

    list_of_tname_tnum_tuples = list(set_of_tname_tnum_tuples.keys())
    random.shuffle(list_of_tname_tnum_tuples)
    blind_identifier_lookup_table = {(num, name): (idx, f"c0ffee{idx^0xFFFF:04x}",) for  idx, (num, name) in enumerate(list_of_tname_tnum_tuples)}
    with Progress() as progress:
        progress_tracker = progress.add_task("[yellow]creating stdfs...", total=len(files))
        state = (set_of_tname_tnum_tuples, blind_identifier_lookup_table, None, set())
        for si in files:
            si_ftype = pathlib.Path(si).suffix
            so = pathlib.Path(odir) / pathlib.Path(si).name
            with _opener[si_ftype](si, "rb") as f, _opener[si_ftype](so, "wb") as out_f:
                (set_of_tname_tnum_tuples, blind_identifier_lookup_table, _, already_logged) = state
                state = (set_of_tname_tnum_tuples, blind_identifier_lookup_table, out_f, already_logged)
                try:
                    while True:
                        b, c = get_construct_and_bytes(f)
                        state = generate_result(state, c, b)
                except endScanning:
                    pass
                except Exception as e:
                    error_console.print(e)
            progress.update(progress_tracker, advance=1)


if __name__ == '__main__':
    main()
