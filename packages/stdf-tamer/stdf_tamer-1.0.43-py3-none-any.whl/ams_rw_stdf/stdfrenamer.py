"""Renames stdf based on MIR conntent

This has the full power of python fstring formating...


Usage:
  stdfrenamer <stdf_file_name_in>  --format="{MIR_LOT_ID}_{MIR_PART_TYP}.stdf" [--check-convention]

Options:
  -h --help               Show this screen.
  --format="fmt string"   A python fstring type format string. The modules datetime, zoneinfo, uuid and random are available
  --check-convention      dont rename just check if the name is in compliance
  stdf_file_name_in       python globs are allowed to select multiple input files (https://docs.python.org/3/library/glob.html)

"""


import ams_rw_stdf
from docopt import docopt
from ams_rw_stdf._opener_collection import _opener
import pathlib
import shutil
import glob
import datetime
import zoneinfo
import uuid
import random
from rich.console import Console
error_console = Console(stderr=True, style="bold red")
console = Console()


def worker(iFilename, fmt, check_compliance):
    iFilename = pathlib.Path(iFilename)
    ftype = iFilename.suffix
    globals_for_eval = {"datetime": datetime,
                        "zoneinfo": zoneinfo,
                        "uuid": uuid,
                        "random": random}
    with _opener[ftype](iFilename, "rb") as f:
        parser = ams_rw_stdf.compileable_RECORD.compile()
        while True:
             c = parser.parse(ams_rw_stdf.get_record_bytes(f))
             if c.REC_TYP == 1 and c.REC_SUB == 10:
                globals_for_eval = globals_for_eval | {f"MIR_{key}": value for key, value in dict(c.PL).items()}
                break
    targetFileName = eval(fmt, globals_for_eval)
    dest = pathlib.Path(targetFileName).expanduser().absolute()
    if check_compliance:
        if iFilename.name != dest.name:
            error_console.print(f"rules violated: {iFilename.name}/{dest.name}/{targetFileName}XXXX{fmt}")
        else:
            console.print(f"{iFilename} OK")
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(iFilename, dest)
        console.print(f"{dest} OK")


def main():
    arguments = docopt(__doc__)
    fmt = f"""f'''{arguments["--format"]}'''"""
    for item in glob.iglob(arguments["<stdf_file_name_in>"], recursive=True):
        worker(item, fmt, arguments["--check-convention"])
        

if __name__ == '__main__':
    main()

