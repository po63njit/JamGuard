# PolarFire SoC Interface Map

## Objective
Define the minimum interface set between the Raspberry Pi 5, KrakenSDR data path, and the PolarFire SoC so integration work can proceed against a shared target.

## System roles
- Raspberry Pi 5: supervisory control, logging, storage, operator interface, non-real-time processing
- PolarFire SoC: deterministic low-latency processing, selected beamforming/filtering kernels, mode control support
- KrakenSDR: coherent multi-channel RF data source

## Interfaces to define
| Interface | Direction | Purpose | Status |
|---|---|---|---|
| Pi to PolarFire control | Bidirectional | mode selection, configuration, health, synchronization commands | To be finalized |
| Pi to PolarFire data movement | Bidirectional | selected data transfer for acceleration and result return | To be finalized |
| KrakenSDR to host ingest | Inbound to Pi path | coherent capture and logging baseline | Working on host side |
| Calibration constant loading | Pi to PolarFire | transfer of channel correction values | Not yet defined |
| Result/status telemetry | PolarFire to Pi | metrics, state, and debug visibility | Not yet defined |

## Immediate decisions required
- communication method between Pi and PolarFire
- data framing format
- which stage receives full-rate versus reduced-rate data
- how timestamps and metadata are preserved across the interface
