from __future__ import annotations
import numpy as np

def normalized_xcorr_lag(x_ref: np.ndarray, x: np.ndarray, max_lag: int) -> tuple[int, float]:
    n = min(len(x_ref), len(x))
    xr, xa = x_ref[:n], x[:n]
    lags = range(-max_lag, max_lag + 1)
    best_lag, best = 0, -1.0
    den = np.linalg.norm(xr) * np.linalg.norm(xa) + 1e-12
    for lag in lags:
        if lag >= 0:
            a, b = xr[lag:], xa[: n - lag]
        else:
            a, b = xr[: n + lag], xa[-lag:]
        c = abs(np.vdot(a, b)) / den
        if c > best:
            best, best_lag = float(c), lag
    return best_lag, best

def windowed_lag_analysis(X: np.ndarray, fs: float, window_samples: int, hop_samples: int, ref_ch: int = 0) -> list[dict]:
    out=[]
    for start in range(0, X.shape[1]-window_samples+1, hop_samples):
        w=X[:,start:start+window_samples]
        for ch in range(X.shape[0]):
            if ch==ref_ch: continue
            lag,corr=normalized_xcorr_lag(w[ref_ch],w[ch],max_lag=32)
            out.append({"start":start,"ch":ch,"lag":lag,"corr":corr,"time_s":start/fs})
    return out

def coherence_score(X: np.ndarray, ref_ch: int = 0) -> float:
    vals=[]
    for ch in range(X.shape[0]):
        if ch==ref_ch: continue
        _,c=normalized_xcorr_lag(X[ref_ch],X[ch],32)
        vals.append(c)
    return float(np.mean(vals)) if vals else 1.0
