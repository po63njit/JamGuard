from pathlib import Path
import csv
import json
from jamguard.io.cfile import read_complex64_cfile
from jamguard.workflow import check_capture_files, channel_health, coarse_lag, multi_window, phase_align, inject_jammer, run_lcmv


def test_pipeline_smoke(tmp_path: Path):
    cap = tmp_path / 'cap'
    # inline synthetic generation equivalent to CLI
    import numpy as np
    from jamguard.io.cfile import write_complex64_cfile
    fs=2_000_000
    t=np.arange(4096)/fs
    cap.mkdir()
    for ch in range(5):
        write_complex64_cfile(cap/f'ch{ch}.cfile',(0.7*np.exp(1j*(2*np.pi*25_000*t+ch*0.2))).astype(np.complex64))

    assert len(check_capture_files(cap))==5
    assert len(channel_health(cap, fs))==5
    assert len(coarse_lag(cap, fs))==4
    assert len(multi_window(cap, fs, max_samples=2048))>0
    phase_align(cap, tmp_path/'aligned', force=True)
    jam = tmp_path/'jammed'
    manifest = inject_jammer(tmp_path/'aligned', jam, fs, force=True)
    assert manifest['amplitude'] > 0
    metrics_csv = tmp_path/'metrics.csv'
    run_lcmv(jam, tmp_path/'lcmv', metrics_csv, fs, force=True)
    out = tmp_path/'lcmv'/'lcmv_ch0ref_null.cfile'
    assert out.exists()
    y = read_complex64_cfile(out)
    assert y.dtype.name == 'complex64' and len(y)>0
    assert metrics_csv.exists()
    assert (tmp_path/'lcmv'/'weights.json').exists()
    _=next(csv.DictReader(metrics_csv.open()))
    _=json.loads((tmp_path/'lcmv'/'weights.json').read_text())
