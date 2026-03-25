# Channel Health Checks

## Goal
Detect whether the five-channel coherent capture path is stable enough to support later beamforming work.

## Initial checks
- verify all expected channels are present
- verify amplitude levels are within a reasonable spread
- verify no channel is consistently saturated or dead
- verify phase relationships are stable over repeated short runs
- verify timing alignment is consistent with the SDR health indicators

## Outputs to record
- per-channel power summary
- phase stability observation
- timestamp and capture identifier
- pass/fail or review-needed decision

## Minimum definition of pass
- all channels present
- no obvious failed channel
- repeated captures show comparable health behavior
