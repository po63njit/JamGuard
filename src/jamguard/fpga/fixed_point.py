from __future__ import annotations
from pathlib import Path
import numpy as np

def _parse_q(q_format:str)->tuple[int,int]:
    i,f=q_format.lower().replace('q','').split('.')
    return int(i),int(f)

def quantize_complex(x:np.ndarray,q_format:str='q1.15')->np.ndarray:
    _,fb=_parse_q(q_format)
    s=2**fb
    lim=s-1
    xr=np.clip(np.round(np.real(x)*s),-s,lim).astype(np.int16)
    xi=np.clip(np.round(np.imag(x)*s),-s,lim).astype(np.int16)
    return np.column_stack((xr,xi))

def dequantize_complex(iq:np.ndarray,q_format:str='q1.15')->np.ndarray:
    _,fb=_parse_q(q_format)
    s=2**fb
    return (iq[:,0]/s + 1j*iq[:,1]/s).astype(np.complex64)

def write_hex_vector(path:str|Path, values:np.ndarray)->None:
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w') as f:
        for r,i in values:
            f.write(f"{(int(r)&0xffff):04x}{(int(i)&0xffff):04x}\n")

def read_hex_vector(path:str|Path,q_format:str='q1.15')->np.ndarray:
    rows=[]
    for ln in Path(path).read_text().splitlines():
        if not ln.strip(): continue
        r=int(ln[:4],16); i=int(ln[4:8],16)
        if r>=0x8000: r-=0x10000
        if i>=0x8000: i-=0x10000
        rows.append((r,i))
    return dequantize_complex(np.array(rows,dtype=np.int16),q_format)
