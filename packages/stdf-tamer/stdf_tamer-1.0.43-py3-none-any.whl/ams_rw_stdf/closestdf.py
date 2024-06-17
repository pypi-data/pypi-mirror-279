"""Closing stdf file.

This is necessary due to the exisitance of STDF writers, which
do not ensure that STDFs are valid at all times...

Usage:
  closestdf <infile> <outfile>
  
Options:
  -h --help     Show this screen.
"""
from docopt import docopt
import ams_rw_stdf
import pathlib
from ams_rw_stdf._opener_collection import _opener
import collections
from datetime import datetime
from datetime import timezone
from rich import print

PFs = collections.defaultdict(lambda: "F", {1: "P"})
try:
    parse = ams_rw_stdf.RECORD.compile()
except Exception:
    parse = ams_rw_stdf.RECORD

def main():
    arguments = docopt(__doc__)
    hBinCounter = collections.defaultdict(lambda: 0)
    sBinCounter = collections.defaultdict(lambda: 0)
    si_ftype = pathlib.Path(arguments["<infile>"]).suffix
    with _opener[si_ftype](arguments["<infile>"], "rb") as f, _opener[si_ftype](arguments["<outfile>"], "wb") as of:
        finishWritten = hbinWritten = sbinWritten = finishWritten = part_closed = False
        site_list = []
        head_list = []
        while True:
            try:
                c = parse.parse(ams_rw_stdf.get_record_bytes(f))
                if c["REC_TYP"] == 5 and c["REC_SUB"] == 20:
                    hBinCounter[(c.PL.HARD_BIN, c.PL.SITE_NUM, c.PL.HEAD_NUM)]  += 1
                    sBinCounter[(c.PL.SOFT_BIN, c.PL.SITE_NUM, c.PL.HEAD_NUM)]  += 1
                if c["REC_TYP"] == 5 and c["REC_SUB"] == 10:
                    head_list.append(c["PL"]["HEAD_NUM"])
                    site_list.append(c["PL"]["SITE_NUM"])

                part_closed   = (c["REC_TYP"] == 5 and c["REC_SUB"] == 20) or part_closed
                hbinWritten   = (c["REC_TYP"] == 1 and c["REC_SUB"] == 40) or hbinWritten
                sbinWritten   = (c["REC_TYP"] == 1 and c["REC_SUB"] == 50) or sbinWritten
                finishWritten = (c["REC_TYP"] == 1 and c["REC_SUB"] == 20) or finishWritten
                of.write(ams_rw_stdf.RECORD.build(c))
            except Exception as e:
                print(e)
                break

        if not finishWritten:
            print("Modifying stdf file by adding some records")
            if not part_closed:
                print("Adding PRR record")
                for (site, head) in zip(site_list, head_list):
                    of.write(ams_rw_stdf.RECORD.build({'REC_LEN': 10, 'REC_TYP': 5, 'REC_SUB': 20, 'PL': 
                                                   {"HEAD_NUM": head, "SITE_NUM": site, "PART_FLG": 0, "NUM_TEST": 0, "HARD_BIN": 0, "SOFT_BIN": 0,
                                                    "X_COORD": 0,"Y_COORD": 0,"TEST_T": 0,"PART_ID": "closer added dummy",
                                                    "PART_TXT": "closer added dummy","PART_FIX": "closer added dummy",}}))
            if not hbinWritten:
                print("Adding hw bin information")
                for (binNr, snum, hnum), binCnt in hBinCounter.items():
                    of.write(ams_rw_stdf.RECORD.build({'REC_LEN': 10, 'REC_TYP': 1, 'REC_SUB': 40, 'PL': 
                                                       {'HEAD_NUM': hnum, 'SITE_NUM': snum, 'HBIN_NUM': binNr, 'HBIN_CNT': binCnt, 'HBIN_PF':  PFs[binNr], "HBIN_NAM": f"HBIN_{binNr}"}}))
            if not sbinWritten:
                print("Adding sw bin information")
                for (binNr, snum, hnum), binCnt in sBinCounter.items():
                    of.write(ams_rw_stdf.RECORD.build({'REC_LEN': 10, 'REC_TYP': 1, 'REC_SUB': 50, 'PL': 
                                                        {'HEAD_NUM': hnum, 'SITE_NUM': snum, 'SBIN_NUM': binNr, 'SBIN_CNT': binCnt, 'SBIN_PF':  PFs[binNr], "SBIN_NAM": f"SBIN_{binNr}"}}))
            print("Adding MRR record")
            of.write(ams_rw_stdf.RECORD.build({'REC_LEN': 10, 'REC_TYP': 1, 'REC_SUB': 20, 'PL': 
                                               {'FINISH_T': int(datetime.now(timezone.utc).timestamp()), 'DISP_COD': " ", 'USR_DESC': '', 'EXC_DESC': ''}}))


if __name__ == '__main__':
    main()
