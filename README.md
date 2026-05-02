# COTS Anti-Jamming GNSS Beamforming System (JamGuard)

Minimal end-to-end JamGuard pipeline for 5-channel GNSS IQ captures (`complex64` `.cfile`).

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
pip install -e .
```

## Synthetic smoke workflow
```bash
python scripts/analysis/create_synthetic_5ch_capture.py --output-dir data/raw/synth_smoke --force
python scripts/analysis/check_capture_files.py --input-dir data/raw/synth_smoke --output results/tables/synth_check.json
python scripts/analysis/channel_health_summary.py --input-dir data/raw/synth_smoke --output results/tables/synth_health.json --sample-rate 2000000
python scripts/analysis/coarse_sample_lag_check.py --input-dir data/raw/synth_smoke --output results/tables/synth_lag.json --sample-rate 2000000
python scripts/analysis/multi_window_coherence.py --input-dir data/raw/synth_smoke --output results/tables/synth_coherence.json --sample-rate 2000000
python scripts/analysis/phase_align_channels.py --input-dir data/raw/synth_smoke --output-dir data/processed/synth_phase --force
python scripts/beamforming/inject_synthetic_jammer.py --input-dir data/processed/synth_phase --output-dir data/processed/synth_synth_jam --sample-rate 2000000 --force
python scripts/beamforming/run_lcmv_nuller.py --input-dir data/processed/synth_synth_jam --output-dir data/processed/synth_lcmv --metrics-csv results/tables/synth_lcmv_metrics.csv --sample-rate 2000000 --force
python scripts/gnss_sdr/make_gnss_sdr_config.py --input-cfile data/processed/synth_lcmv/lcmv_ch0ref_null.cfile --output configs/gnss_sdr/synth_lcmv.conf --sample-rate 2000000
python scripts/reports/make_master_results_table.py --run-name synth --lcmv-metrics results/tables/synth_lcmv_metrics.csv --jam-manifest data/processed/synth_synth_jam/manifest.json --output results/tables/synth_master_results.csv
```


> **Sample-rate requirement:** Always pass the **actual capture sample rate** to scripts that consume timing/frequency data (`--sample-rate`), unless metadata manifest provides it. Do **not** rely on 2,000,000 as a default for real captures. In this KrakenSDR workflow, common values are **2,048,000** and **2,400,000** samples/sec.

## Safety
Use only offline synthetic or fully conducted/shielded jammer tests. Do not radiate GNSS interference.


## test_110 result snapshot (capstone)
- Dataset: `/media/patryk/X31/test_110` (real 5-channel KrakenSDR capture, 2.4 MSPS).
- 180 s LCMV output suppressed the controlled injected jammer bin by ~97.18 dB.
- GNSS-SDR validation on 180 s LCMV output: tracking present, 119 NAV messages, position fix achieved.
- Robust synthetic sweep (CW/chirp/wideband noise) summary is generated with `scripts/reports/analyze_test_110_robust_sweep_spectral.py`.

See `docs/09_test_110_robust_sweep_workflow.md` for runbook, troubleshooting, and report-safe claim boundaries.
