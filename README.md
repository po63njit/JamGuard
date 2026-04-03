# JamGuard MVP

JamGuard is a **real, runnable offline Python MVP** for coherent 5-channel KrakenSDR GNSS capture analysis.

It focuses on immediately useful capstone work:
- channel health diagnostics
- PSD/correlation/phase checks
- basic relative channel calibration
- UCA steering vector + fixed delay-and-sum beamforming
- synthetic directional tone jammer injection
- one-command demo pipeline producing figures + JSON summary artifacts

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Configure your capture

Edit `configs/default_experiment.yaml` and replace `channel_files` with your real simultaneous files:

```yaml
channel_files:
  - /path/to/ch0.cf32
  - /path/to/ch1.cf32
  - /path/to/ch2.cf32
  - /path/to/ch3.cf32
  - /path/to/ch4.cf32
```

CF32 assumption: each file is complex64 IQ, one file per channel, same sample count.

## CLI commands

```bash
jamguard inspect --config configs/default_experiment.yaml
jamguard plot-psd --config configs/default_experiment.yaml
jamguard compare-channels --config configs/default_experiment.yaml
jamguard calibrate --config configs/default_experiment.yaml
jamguard beamform --config configs/default_experiment.yaml --azimuth-deg 0
jamguard inject-jammer --config configs/default_experiment.yaml --tone-hz 100000 --amplitude 3 --azimuth-deg 60
jamguard demo-pipeline --config configs/default_experiment.yaml --tone-hz 100000 --amplitude 3 --jammer-azimuth-deg 60 --look-azimuth-deg 0
```

## Artifacts generated in `output_dir`

- `channel_power.png`
- `psd_comparison.png`
- `correlation_heatmap.png`
- `phase_offsets.png`
- `beam_pattern.png`
- `beamforming_before_after_psd.png`
- `calibration.json` (from `calibrate`)
- `beamformed_output.npy` (from `beamform`)
- `demo_summary.json`

## Thin scripts

```bash
python scripts/run_channel_health.py --config configs/default_experiment.yaml
python scripts/run_calibration_summary.py --config configs/default_experiment.yaml
python scripts/run_first_beamforming_demo.py --config configs/default_experiment.yaml
```

## Tests

```bash
pytest -q
```

## Notes / TODO

- Null-steering and adaptive MVDR are intentionally deferred for post-MVP work.
- Current beamforming is conventional fixed steering.
- This offline MVP is intended as the algorithm reference for later FPGA/SoC migration.
