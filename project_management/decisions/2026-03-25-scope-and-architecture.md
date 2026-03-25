# Decision: Scope and Architecture Reset

## Problem
The original wearable framing risked spreading effort across packaging, sensors, and user-interface features before the core anti-jam GNSS path was validated.

## Decision
Treat the semester build as a portable anti-jam GNSS prototype centered on coherent capture, calibration, beamforming, and FPGA integration.

## Rationale
- This matches the March 13, 2026 project revision.
- It keeps the PolarFire SoC central without forcing premature full-system complexity.
- It aligns the schedule with a realistic one-person capstone critical path.

## Consequences
- Wearable packaging becomes future product context, not the current main build target.
- The first hard milestone is a stable five-antenna coherent array.
- Documentation, testing, and code should all map to the Pi plus KrakenSDR plus PolarFire architecture.
