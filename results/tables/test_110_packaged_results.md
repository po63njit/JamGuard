# test_110 packaged anti-jam results

## Summary table

| segment_s | samples | output_power_db | rms | covariance_condition_number | jammer_bin_before_db | jammer_bin_after_db | jammer_suppression_db | gnss_tracking_events | unique_prns_tracked | nav_messages | position_fix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10 | 24000000 | -23.029 | 0.071 | 17970.399 | 67.260 | -23.070 | 90.330 | 4 | 4 | 0 | No |
| 60 | 144000000 | -18.434 | 0.120 | 29955.023 | 72.910 | -19.090 | 92.000 | 10 | 7 | 21 | No |
| 180 | 432000000 | -21.971 | 0.080 | 2023.774 | 72.910 | -24.270 | 97.180 | 11 | 8 | 119 | Yes |

## Lead result

The strongest result is the 180-second LCMV run:

- Processed samples: 432,000,000 complex64 samples
- Jammer-bin suppression: 97.18 dB
- GNSS-SDR tracking-start events: 11
- Unique GPS L1 C/A PRNs tracked: 8
- GPS NAV messages decoded: 119
- GNSS-SDR position fix: yes

## Report-safe conclusion

A real five-channel KrakenSDR GNSS capture was phase-aligned, injected with a controlled synthetic spatial narrowband jammer, processed through an LCMV/nulling beamformer, and exported as a GNSS-SDR-compatible complex64 stream.

In the 180-second run, the beamformer suppressed the injected jammer bin by approximately 97.2 dB while preserving enough GPS L1 C/A signal structure for GNSS-SDR to track multiple satellites, decode 119 NAV messages, and compute a position fix.

This should be presented as controlled synthetic narrowband spatial jammer suppression on real captured GNSS data, not as a claim of immunity against arbitrary real-world jamming or as a direct claim of outperforming commercial CRPA anti-jam systems.
