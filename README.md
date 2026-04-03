# JamGuard

JamGuard is an **offline Python analysis backbone** for coherent GNSS array captures focused on beamforming and anti-jam experimentation before FPGA acceleration.

## Current Capstone Scope
- KrakenSDR coherent 5-channel capture ingest (one file per channel initially)
- Channel health/coherence diagnostics
- Phase/delay estimation and calibration scaffolding
- UCA steering vector and beamforming scaffolding
- Reporting and experiment logging stubs for reproducibility

## Quick Start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest -q
```

## CLI (Scaffold)
```bash
jamguard inspect --config configs/default_experiment.yaml
jamguard summarize --config configs/default_experiment.yaml
jamguard beamform --config configs/default_experiment.yaml
```

> Note: CLI subcommands are intentionally scaffolded and raise `NotImplementedError` until pipeline functions are implemented.

## Repository Layout
- `src/jamguard/`: package source
- `tests/`: unit/integration tests
- `configs/`: experiment configurations
- `scripts/`: wrapper scripts for recurring experiment flows
- `docs/`: architecture and development planning docs
- `data/`, `results/`: local data and generated artifacts
