# test_110 60-second anti-jam result

## Dataset

- Raw dataset: `/media/patryk/X31/test_110`
- Sample rate: 2.4 MSPS
- Channels: 5
- Raw capture length: 600 seconds
- Processed slice: first 60 seconds
- Samples per processed channel: 144,000,000

## Processing chain

1. Loaded first 60 seconds from 5 coherent KrakenSDR channel files.
2. Applied phase alignment relative to CH0.
3. Injected a synthetic spatial narrowband jammer.
4. Ran LCMV/nulling beamformer.
5. Exported a single complex64 beamformed output file.
6. Ran GNSS-SDR on the LCMV output.

## LCMV output validation

- Output file: `/media/patryk/X31/jamguard_processed_test110/test_110_lcmv_60s/lcmv_ch0ref_null.cfile`
- Samples: 144,000,000
- Duration: 60.0 seconds
- Sample rate: 2.4 MSPS
- Output power: -18.43 dB
- RMS: 0.11976
- NaN/Inf count: 0
- Covariance condition number: 29,955

## Narrowband jammer suppression

- Jammer offset: 1.5 kHz
- Jammer amplitude: 3.0
- Jammer bin before nulling: 72.91 dB
- Jammer bin after nulling: -19.09 dB
- Suppression: 92.00 dB

## GNSS-SDR validation

GNSS-SDR successfully processed the 60-second LCMV output.

Unique GPS L1 C/A PRNs tracked:

- PRN 01
- PRN 03
- PRN 06
- PRN 14
- PRN 19
- PRN 21
- PRN 22

GNSS-SDR reported 10 tracking-start events in the 60-second LCMV run.

GNSS-SDR also decoded multiple GPS NAV subframes from the processed LCMV output, including satellites with reported CN0 values approximately in the 37–43 dB-Hz range.

Representative decoded NAV messages:

- PRN 06: CN0 approximately 37–39 dB-Hz
- PRN 19: CN0 approximately 37–40 dB-Hz
- PRN 14: CN0 approximately 41–43 dB-Hz
- PRN 01: CN0 approximately 40–41 dB-Hz
- PRN 03: CN0 approximately 39 dB-Hz
- PRN 22: CN0 approximately 38 dB-Hz

## Report-safe conclusion

The 60-second test_110 experiment demonstrates that the COTS five-channel GNSS array capture can be phase-aligned, synthetically jammed with a controlled spatial narrowband interferer, processed using an LCMV/nulling beamformer, and exported as a GNSS-SDR-compatible complex64 stream.

The LCMV pipeline suppressed the injected narrowband jammer bin by approximately 92 dB while preserving enough GNSS signal structure for GNSS-SDR to track multiple GPS L1 C/A satellites and decode NAV subframes from the processed output.

This should be presented as controlled synthetic narrowband spatial jammer suppression on real captured GNSS data, not as a claim of immunity against arbitrary real-world jamming.
