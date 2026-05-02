# Signal analysis pathway

JamGuard expects a preserved 5-channel capture folder with files:
`ch0.cfile` .. `ch4.cfile` (complex64 interleaved IQ).

## End-to-end command flow

1) Validate files:
`python scripts/analysis/check_capture_files.py --input <capture_dir> --output results/tables/check_capture.json --channels 5 --pattern 'ch{}.cfile'`

2) Channel health:
`python scripts/analysis/channel_health_summary.py --input <capture_dir> --output results/tables/channel_health.json --sample-rate 2000000`

3) Coherence/timing:
- `python scripts/analysis/coarse_sample_lag_check.py --input <capture_dir> --output results/tables/coarse_lag.json --sample-rate 2000000`
- `python scripts/analysis/multi_window_coherence.py --input <capture_dir> --output results/tables/window_coherence.json --sample-rate 2000000 --max-samples 200000`

4) Phase alignment:
`python scripts/analysis/phase_align_channels.py --input <capture_dir> --output-dir data/processed/<run_name>_phase --force`

5) Jammer injection:
`python scripts/beamforming/inject_synthetic_jammer.py --input data/processed/<run_name>_phase --output-dir data/processed/<run_name>_synth_jam --sample-rate 2000000 --force`

6) LCMV nulling:
`python scripts/beamforming/run_lcmv_nuller.py --input data/processed/<run_name>_synth_jam --output-dir data/processed/<run_name>_lcmv --metrics-csv results/tables/<run_name>_lcmv_metrics.csv --sample-rate 2000000 --force`
