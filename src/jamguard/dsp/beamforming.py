from __future__ import annotations
import numpy as np

def wavelength(freq_hz:float,c:float=299792458.0)->float:
    return c/freq_hz

def uca_positions(num_elements:int,radius_m:float)->np.ndarray:
    ang=np.linspace(0,2*np.pi,num_elements,endpoint=False)
    return np.column_stack((radius_m*np.cos(ang),radius_m*np.sin(ang),np.zeros(num_elements)))

def steering_vector_uca(num_elements:int,radius_m:float,azimuth_deg:float,freq_hz:float)->np.ndarray:
    pos=uca_positions(num_elements,radius_m)
    lam=wavelength(freq_hz)
    az=np.deg2rad(azimuth_deg)
    k=np.array([np.cos(az),np.sin(az),0.0])
    phase=-2j*np.pi/lam*(pos@k)
    return np.exp(phase)

def covariance_matrix(X:np.ndarray, diagonal_loading:float=0.0)->np.ndarray:
    R=(X@X.conj().T)/X.shape[1]
    if diagonal_loading>0: R=R+diagonal_loading*np.eye(X.shape[0])
    return R

def mvdr_weights(R:np.ndarray,a_look:np.ndarray)->np.ndarray:
    Ri=np.linalg.pinv(R)
    num=Ri@a_look
    den=a_look.conj().T@num
    return num/den

def lcmv_weights(R:np.ndarray,C:np.ndarray,f:np.ndarray)->np.ndarray:
    Ri=np.linalg.pinv(R)
    M=np.linalg.pinv(C.conj().T@Ri@C)
    return Ri@C@M@f

def apply_weights(X:np.ndarray,w:np.ndarray)->np.ndarray:
    return np.sum(np.conj(w)[:,None]*X,axis=0)
