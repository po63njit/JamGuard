from __future__ import annotations
from pathlib import Path
import re

def parse_gnss_sdr_log(path:str|Path)->dict:
    txt=Path(path).read_text(errors='ignore')
    acq=re.findall(r'Acquisition|ACQ',txt)
    trk=re.findall(r'Track|TRACK',txt)
    pvt=re.findall(r'PVT|position solution',txt,re.I)
    cn0=[float(x) for x in re.findall(r'([0-9]+\.?[0-9]*)\s*dB-?Hz',txt)]
    return {"path":str(path),"acquisition_events":len(acq),"tracking_events":len(trk),"pvt_events":len(pvt),"cn0_values":cn0,"cn0_mean":(sum(cn0)/len(cn0) if cn0 else None)}

def summarize_gnss_sdr_runs(log_paths:list[str])->list[dict]:
    return [parse_gnss_sdr_log(p) for p in log_paths]
