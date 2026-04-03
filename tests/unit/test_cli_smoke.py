import os
import subprocess
import sys


def test_cli_help() -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = f"src:{env.get('PYTHONPATH', '')}"
    proc = subprocess.run(
        [sys.executable, "-m", "jamguard.cli.main", "-h"],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    assert proc.returncode == 0
    assert "inspect" in proc.stdout
