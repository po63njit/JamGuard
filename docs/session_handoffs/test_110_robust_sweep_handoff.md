# test_110 robust anti-jam workflow handoff

## Project context

Project: COTS Anti-Jamming GNSS Beamforming System

Hardware/data source:
- 5-channel KrakenSDR coherent GNSS capture
- Real GPS L1 C/A capture: `/media/patryk/X31/test_110`
- Sample rate: 2.4 MSPS
- Channels: 5
- Full raw capture length: 600 s
- Robust processing segment: 180 s
- 180 s samples per channel: 432,000,000 complex64 samples

## Main validated result before robust sweep

A 180-second LCMV output was generated from real captured GNSS data with a controlled synthetic spatial narrowband jammer.

Output:
`/media/patryk/X31/jamguard_processed_test110/test_110_lcmv_180s/lcmv_ch0ref_null.cfile`

Metrics:
- Samples: 432,000,000
- Duration: 180 s
- Output power: -21.9707 dB
- RMS: 0.07970
- Covariance condition number: 2023.77
- Jammer bin before nulling: 72.91 dB
- Jammer bin after nulling: -24.27 dB
- Jammer suppression: 97.18 dB

GNSS-SDR validation:
- GNSS-SDR successfully processed the LCMV output.
- Unique GPS L1 C/A PRNs tracked: 01, 02, 03, 06, 11, 14, 19, 21
- Tracking-start events: 11
- GPS NAV messages decoded: 119
- Position fix achieved: yes

Report-safe conclusion:
This demonstrates controlled synthetic narrowband spatial jammer suppression on real captured GNSS data, while preserving enough GNSS structure for GNSS-SDR tracking, NAV decode, and a position fix. It should not be claimed as arbitrary real-world jamming immunity.

## Robust synthetic jammer sweep

Goal:
Create more realistic stress tests using multiple jammer types and amplitudes.

Sweep cases:
- Jammer kinds: `cw`, `chirp`, `wideband_noise`
- Amplitudes: `3`, `8`, `16`
- Segment length: 180 s
- Input: phase-aligned 5-channel real GNSS capture
- Branches:
  - jammed single-channel CH0 baseline
  - LCMV/nulling output

Important GNSS-SDR issue:
GNSS-SDR repeatedly stalled when run inside the robust sweep, especially on jammed CH0 and some LCMV batch cases. The logs stopped near:
`GNSS signal recorded time to be processed: 179.9 [s]`

Interpretation:
Strong/interfered files can block GNSS-SDR acquisition before receiver-time processing starts. GNSS-SDR is useful for selected validation outputs, but it is fragile as an inner-loop metric for all stress cases.

Temporary workaround:
The sweep script was patched to skip GNSS-SDR inside the per-case loop and rely on spectral metrics for the robust sweep.

## Robust spectral metrics

Generated files:
- `results/tables/test_110_robust_spectral_metrics.csv`
- `results/tables/test_110_robust_spectral_metrics.md`
- `results/figures/test_110_robust_primary_suppression.png`

Summary table from spectral analysis:

| Jammer | Amp | Primary metric | Primary suppression dB | Tone 1.5 kHz suppression dB | ±500 kHz suppression dB | Fullband PSD reduction dB | Time-power reduction dB |
|---|---:|---|---:|---:|---:|---:|---:|
| cw | 3 | tone_1500_suppression_db | 84.148 | 84.148 | 35.003 | 31.573 | 31.524 |
| cw | 8 | tone_1500_suppression_db | 92.735 | 92.735 | 43.739 | 40.315 | 40.272 |
| cw | 16 | tone_1500_suppression_db | 98.697 | 98.697 | 49.795 | 46.373 | 46.330 |
| chirp | 3 | wide_pm500k_suppression_db | 35.006 | 41.544 | 35.006 | 31.576 | 31.527 |
| chirp | 8 | wide_pm500k_suppression_db | 43.741 | 50.158 | 43.741 | 40.318 | 40.275 |
| chirp | 16 | wide_pm500k_suppression_db | 49.795 | 56.126 | 49.795 | 46.373 | 46.330 |
| wideband_noise | 3 | fullband_avg_psd_reduction_db | 3.968 | 2.895 | 3.893 | 3.968 | 3.908 |
| wideband_noise | 8 | fullband_avg_psd_reduction_db | 40.466 | 38.641 | 40.066 | 40.466 | 40.420 |
| wideband_noise | 16 | fullband_avg_psd_reduction_db | 46.407 | 44.508 | 46.015 | 46.407 | 46.362 |

Important interpretation:
- CW and chirp cases show strong spatial suppression.
- Wideband noise amp=3 shows weak suppression compared with higher amplitudes and needs careful discussion.
- The robust sweep should be reported as controlled synthetic spatial-interference suppression, not as direct comparison to commercial CRPA performance.

## Code/workflow issues to fix

1. The robust sweep script currently has GNSS-SDR skipped inside the loop. This should be intentional and documented, not an accidental patch.
2. Need a clean separation between:
   - spectral robust sweep
   - selected GNSS-SDR validation runs
3. Need scripts that avoid generating/keeping huge intermediate `.cfile` files unless explicitly requested.
4. Need consistent environment variables:
   - `KEEP_CFILES`
   - `RESET_SUMMARY`
   - `JAMMER_KINDS_STR`
   - `AMPS_STR`
   - `MAX_SAMPLES`
   - `FS`
5. Need documentation explaining why GNSS-SDR is not used as the primary metric for every jammed robust case.
6. Need report-ready tables and figures packaged under `results/`.
7. Need a safer GNSS-SDR runner that times out cleanly, kills child processes, and does not leave zombie/stopped `gnss-sdr`, `timeout`, or `tee` processes.
8. Need a selected-output GNSS-SDR validation script for specific LCMV files only.

## Desired final workflow

Recommended workflow:

1. Validate raw capture health and timing/coherence.
2. Phase-align channels.
3. Run robust synthetic jammer sweep:
   - CW
   - chirp
   - wideband noise
   - multiple amplitudes
4. Compute spectral suppression metrics for every case.
5. Run GNSS-SDR only on selected LCMV outputs:
   - baseline original 180 s LCMV
   - best CW recovery
   - best chirp recovery
   - best wideband recovery if reasonable
6. Generate report package:
   - CSV tables
   - Markdown tables
   - figures
   - logs
   - README explaining interpretation limits
7. Avoid committing raw/generated `.cfile` data.

