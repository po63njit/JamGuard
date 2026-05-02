from __future__ import annotations
import numpy as np

def generate_tone_jammer(num_samples:int, fs:float, offset_hz:float, amplitude:float, phase:float=0.0)->np.ndarray:
    t=np.arange(num_samples)/fs
    return (amplitude*np.exp(1j*(2*np.pi*offset_hz*t+phase))).astype(np.complex64)

def generate_chirp_jammer(num_samples:int, fs:float, f0_hz:float, f1_hz:float, amplitude:float)->np.ndarray:
    t=np.arange(num_samples)/fs
    k=(f1_hz-f0_hz)/(num_samples/fs)
    ph=2*np.pi*(f0_hz*t+0.5*k*t**2)
    return (amplitude*np.exp(1j*ph)).astype(np.complex64)

def inject_spatial_interferer(X:np.ndarray, jammer:np.ndarray, spatial_signature:np.ndarray)->np.ndarray:
    return X + spatial_signature[:,None]*jammer[None,:X.shape[1]]

def estimate_dominant_bin(x:np.ndarray, fs:float)->dict:
    S=np.fft.fftshift(np.fft.fft(x))
    k=int(np.argmax(np.abs(S)))
    f=np.fft.fftshift(np.fft.fftfreq(len(x),d=1/fs))[k]
    return {"bin":k,"freq_hz":float(f),"mag":float(np.abs(S[k]))}
