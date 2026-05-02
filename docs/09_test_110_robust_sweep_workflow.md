# test_110 robust synthetic jammer workflow (report-ready)

## What this proves
- On a real 5-channel KrakenSDR capture (`/media/patryk/X31/test_110`, 2.4 MSPS), controlled synthetic spatial jammers can be strongly suppressed by the LCMV/nulling stage.
- In the 180 s case, the injected jammer bin was reduced by ~97.18 dB and GNSS-SDR decoded NAV and produced a position fix.

## What this does **not** prove
- It does not prove immunity to arbitrary real-world jamming.
- It is not a claim of parity with commercial CRPA anti-jam devices.

## Why GNSS-SDR may appear to stall in jammed cases
Strongly jammed single-channel files can cause long acquisition loops or no lock progress. For robust sweep batch runs, CH0 jammed and LCMV branches may be logged as intentionally skipped, and spectral suppression metrics are used for consistent per-case comparison.

## Runbook
```bash
# 1) Reproduce 180 s LCMV result (manual path)
python scripts/analysis/phase_align_channels.py --input-dir /media/patryk/X31/test_110 --output-dir /media/patryk/X31/jamguard_processed_test110/test_110_phase_180s --channels 5 --pattern 'ch{}.cfile' --max-samples 432000000 --force
python scripts/beamforming/inject_synthetic_jammer.py --input-dir /media/patryk/X31/jamguard_processed_test110/test_110_phase_180s --output-dir /media/patryk/X31/jamguard_processed_test110/test_110_synth_jam_180s --sample-rate 2400000 --channels 5 --max-samples 432000000 --force
python scripts/beamforming/run_lcmv_nuller.py --input-dir /media/patryk/X31/jamguard_processed_test110/test_110_synth_jam_180s --output-dir /media/patryk/X31/jamguard_processed_test110/test_110_lcmv_180s --metrics-csv results/tables/test_110_lcmv_metrics_180s.csv --sample-rate 2400000 --channels 5 --max-samples 432000000 --force

# 2) Reproduce robust spectral sweep
bash scripts/experiments/run_test_110_robust_sweep_180s.sh
python scripts/reports/analyze_test_110_robust_sweep_spectral.py --proc-root /media/patryk/X31/jamguard_processed_test110 --run-name test_110 --sample-rate 2400000

# 3) Regenerate report tables/figures
python scripts/reports/package_test_110_results.py

# 4) Package report artifacts
python scripts/reports/package_results.py --run-name test_110
```
