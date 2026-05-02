# COTS Anti-Jamming GNSS Beamforming System (JamGuard)

Foundation scaffold for capture validation, coherence analysis, jammer injection, beamforming, and GNSS-SDR config/log workflows.

## Architecture
5x GNSS antennas -> KrakenSDR 5ch capture -> IQ `.cfile` -> Python analysis/beamforming -> GNSS-SDR validation -> FPGA handoff vectors.

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
pip install -e .
```

## Sample workflow
```bash
python scripts/analysis/check_capture_files.py --input data/raw/run01 --output results/tables/check.csv
python scripts/analysis/multi_window_coherence.py --input data/raw/run01 --output results/tables/coherence.csv
python scripts/beamforming/inject_synthetic_jammer.py --input data/raw/run01 --output data/processed/jammed.json
python scripts/beamforming/run_lcmv_nuller.py --input data/processed/jammed.json --output data/processed/lcmv.json
python scripts/gnss_sdr/make_gnss_sdr_config.py --input data/processed/lcmv.cfile --output configs/gnss_sdr/lcmv.conf
```

## Safety
Use only offline synthetic or fully conducted/shielded jammer tests. Do not radiate GNSS interference.
