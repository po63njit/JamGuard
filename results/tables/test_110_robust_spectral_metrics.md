# test_110 robust synthetic jammer spectral metrics

These metrics compare the jammed CH0 stream against the LCMV beamformed output for each 180-second test case.

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
