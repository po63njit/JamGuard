import numpy as np
from jamguard.io.cfile import write_complex64_cfile, read_complex64_cfile, cfile_sample_count
from jamguard.dsp.calibration import estimate_phase_correction
from jamguard.dsp.beamforming import steering_vector_uca, apply_weights
from jamguard.gnss.config import replace_signal_source_filename
from jamguard.fpga.fixed_point import quantize_complex, dequantize_complex


def test_cfile_roundtrip(tmp_path):
    x=(np.random.randn(128)+1j*np.random.randn(128)).astype(np.complex64)
    p=tmp_path/'a.cfile'
    write_complex64_cfile(p,x)
    y=read_complex64_cfile(p)
    assert np.allclose(x,y)


def test_sample_count(tmp_path):
    x=np.zeros(33,dtype=np.complex64)
    p=tmp_path/'b.cfile'; write_complex64_cfile(p,x)
    assert cfile_sample_count(p)==33


def test_phase_correction():
    x=np.exp(1j*np.linspace(0,1,1000)).astype(np.complex64)
    y=x*np.exp(1j*0.4)
    c=estimate_phase_correction(x,y)
    z=y*c
    err=np.angle(np.vdot(z,x))
    assert abs(err) < 1e-3


def test_steering_vector_dims():
    a=steering_vector_uca(5,0.1,30,1575.42e6)
    assert a.shape==(5,)


def test_beamformer_shape():
    X=np.ones((5,64),dtype=np.complex64)
    w=np.ones(5,dtype=np.complex64)/5
    y=apply_weights(X,w)
    assert y.shape==(64,)


def test_config_replace():
    txt='SignalSource.filename=old.cfile\n'
    out=replace_signal_source_filename(txt,'new.cfile')
    assert 'new.cfile' in out and 'old.cfile' not in out


def test_fixed_point_sanity():
    x=np.array([0.25+0.5j,-0.5-0.25j],dtype=np.complex64)
    q=quantize_complex(x)
    y=dequantize_complex(q)
    assert np.allclose(x,y,atol=1/2**14)
