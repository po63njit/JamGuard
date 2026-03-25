# System Architecture

## Goal
Define the first stable end-to-end system boundary for JamGuard so hardware, host software, FPGA work, and testing all target the same prototype.

## Planned signal and control path
1. GNSS antennas feed the coherent multi-channel RF front end.
2. KrakenSDR performs synchronized channel capture.
3. Raspberry Pi 5 manages configuration, capture orchestration, storage, and operator control.
4. PolarFire SoC executes selected timing-critical signal-processing kernels.
5. Processed outputs are evaluated through bench and field validation workflows.

## Interfaces to define next
- antenna to front-end interconnect and cable constraints
- KrakenSDR to Pi data and control path
- Pi to PolarFire control and data movement path
- calibration data format
- capture metadata format
- test result schema for report generation

## Open decisions
- which beamforming stages remain host-side versus FPGA-side
- how calibration constants are versioned
- how raw captures are archived outside Git while staying traceable
