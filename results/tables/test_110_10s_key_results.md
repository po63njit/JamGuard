# test_110 10-second anti-jam result

## Dataset

- Raw dataset: `/media/patryk/X31/test_110`
- Sample rate: 2.4 MSPS
- Channels: 5
- Raw capture length: 600 seconds
- Processed slice: first 10 seconds
- Samples per processed channel: 24,000,000

## Raw capture validation

- All 5 channels were present.
- Each raw channel file contained 1,440,000,000 complex64 samples.
- No invalid samples were found in the analyzed 10-second segment.
- Trusted correlation windows showed zero sample lag.

## Channel health, first 10 seconds

| Channel | Power dBFS |
|---|---:|
| CH0 | -21.94 |
| CH1 | -21.04 |
| CH2 | -22.11 |
| CH3 | -25.24 |
| CH4 | -24.33 |

CH3 and CH4 were weaker than CH0/CH1/CH2, with CH3 being the weakest channel.

## Timing/coherence summary

In trusted correlation windows, no nonzero sample lag was observed across the five-channel capture. Nonzero lag estimates only appeared in low-correlation windows and were not treated as valid timing slips.

## Processing

- Phase alignment completed.
- Synthetic spatial narrowband jammer injected.
- Jammer offset: 1.5 kHz
- Jammer amplitude: 3.0
- LCMV/nulling output generated:
  `/media/patryk/X31/jamguard_processed_test110/test_110_lcmv_10s/lcmv_ch0ref_null.cfile`

## LCMV output validation

- Samples: 24,000,000
- Duration: 10.0 seconds
- Output power: -23.03 dB
- RMS: 0.07055
- NaN/Inf count: 0
- Covariance condition number: 17,970.4

## Narrowband jammer suppression

- Jammer bin before nulling: 67.26 dB
- Jammer bin after nulling: -23.07 dB
- Suppression: 90.33 dB

## GNSS-SDR comparison

GNSS-SDR tracking events over 10 seconds:

| Case | Tracking events |
|---|---:|
| Raw CH0 | 6 |
| Synthetic-jammed CH0 | 8 |
| LCMV output | 4 |

The LCMV output was GNSS-SDR compatible and allowed GPS L1 C/A tracking to start. The synthetic narrowband tone jammer did not create a denial condition in the single-channel jammed baseline, so this specific test demonstrates narrowband spatial interference suppression and receiver compatibility rather than full GNSS denial-and-recovery.

## Report-safe conclusion

A real 5-channel GNSS capture was processed with a controlled synthetic spatial narrowband jammer. The offline LCMV/nulling pipeline suppressed the jammer bin by approximately 90.3 dB while preserving a valid GNSS-SDR-compatible complex64 output.

This result demonstrates coherent multi-channel capture, phase alignment, synthetic spatial interference injection, adaptive/nulling beamforming, and downstream GNSS-SDR compatibility. It should be described as narrowband synthetic jammer suppression, not full real-world GNSS jamming immunity.
