from __future__ import annotations
from pathlib import Path
import numpy as np


def cfile_sample_count(path: str | Path) -> int:
    p = Path(path)
    size = p.stat().st_size
    if size % 8 != 0:
        raise ValueError(f"Invalid cfile byte size for {p}: {size} not divisible by 8")
    return size // 8


def read_complex64_cfile(path: str | Path, count: int | None = None, offset: int = 0) -> np.ndarray:
    p = Path(path)
    total = cfile_sample_count(p)
    if offset < 0 or offset > total:
        raise ValueError("offset out of range")
    n = total - offset if count is None else min(count, total - offset)
    data = np.fromfile(p, dtype=np.complex64, count=n, offset=offset * 8)
    return data


def write_complex64_cfile(path: str | Path, x: np.ndarray) -> None:
    p = Path(path)
    arr = np.asarray(x, dtype=np.complex64)
    p.parent.mkdir(parents=True, exist_ok=True)
    arr.tofile(p)


def load_multichannel_capture(input_dir: str | Path, pattern: str = "ch{}.cfile", channels: int = 5, count: int | None = None) -> np.ndarray:
    root = Path(input_dir)
    arrays = []
    for ch in range(channels):
        fp = root / pattern.format(ch)
        if not fp.exists():
            raise FileNotFoundError(fp)
        arrays.append(read_complex64_cfile(fp, count=count))
    return trim_to_common_length(arrays)


def trim_to_common_length(arrays: list[np.ndarray]) -> np.ndarray:
    if not arrays:
        raise ValueError("arrays must be non-empty")
    m = min(len(a) for a in arrays)
    return np.vstack([np.asarray(a)[:m] for a in arrays])
