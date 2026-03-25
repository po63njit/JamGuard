# Coherent Capture Validation Procedure

## Objective
Verify that the first integrated five-channel array setup produces stable coherent captures suitable for calibration and baseline beamforming work.

## Equipment
- Raspberry Pi 5 host
- KrakenSDR
- five-antenna prototype array
- required cabling and power
- any test accessories used during the run

## Pre-checks
- host matches known-good state
- KrakenSDR web UI indicates healthy status
- antenna geometry revision is recorded
- cable set and connector mapping are recorded

## Procedure
1. Assemble the prototype and document the geometry revision.
2. Boot the host and confirm SDR health indicators.
3. Run a short baseline capture.
4. Repeat the capture without disturbing the setup.
5. Inspect channel presence, power spread, and basic repeatability.
6. Record whether the setup is stable enough for calibration work.

## Pass criteria
- all expected channels are present
- no channel appears dead or grossly unstable
- repeated short captures show similar basic behavior
- setup details are documented well enough to reproduce the run

## Outputs
- capture metadata file
- quick-look summary
- screenshots of known-good SDR status
- result note in `tests/bench/results/`
