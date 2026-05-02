import os
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(Path.cwd() / "src") + os.pathsep + env.get("PYTHONPATH", "")
    subprocess.run([sys.executable, *cmd], check=True, env=env)


def test_cli_smoke(tmp_path: Path):
    cap = tmp_path / "cap"
    aligned = tmp_path / "aligned"
    jammed = tmp_path / "jammed"
    lcmv = tmp_path / "lcmv"
    metrics = tmp_path / "metrics.csv"
    conf = tmp_path / "gnss.conf"
    fs = "2048000"

    run(["scripts/analysis/create_synthetic_5ch_capture.py", "--output-dir", str(cap), "--sample-rate", fs, "--force"])
    run(["scripts/analysis/phase_align_channels.py", "--input-dir", str(cap), "--output-dir", str(aligned), "--force"])
    run(["scripts/beamforming/inject_synthetic_jammer.py", "--input-dir", str(aligned), "--output-dir", str(jammed), "--sample-rate", fs, "--force"])
    run(["scripts/beamforming/run_lcmv_nuller.py", "--input-dir", str(jammed), "--output-dir", str(lcmv), "--metrics-csv", str(metrics), "--sample-rate", fs, "--force"])
    run(["scripts/gnss_sdr/make_gnss_sdr_config.py", "--input-cfile", str(lcmv / "lcmv_ch0ref_null.cfile"), "--output", str(conf), "--sample-rate", fs])

    assert (lcmv / "lcmv_ch0ref_null.cfile").exists()
    assert metrics.exists()
    txt = conf.read_text()
    assert "2048000" in txt
    assert str((lcmv / "lcmv_ch0ref_null.cfile").resolve()) in txt
