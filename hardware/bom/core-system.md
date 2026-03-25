# Core System BOM

This is the working bill of materials for the first integrated JamGuard prototype. It is intentionally focused on the minimum viable system needed for coherent capture, host control, and FPGA integration.

| Subsystem | Item | Qty | Role | Status | Notes |
|---|---|---:|---|---|---|
| Host compute | Raspberry Pi 5 starter kit | 1 | System host for orchestration, logging, UI, and networking | Confirmed working | Treat as the primary host platform |
| RF front end | KrakenSDR | 1 | Five-channel coherent SDR front end | Confirmed working | Bring-up completed on Pi 5 image |
| Acceleration | PolarFire SoC Discovery Kit | 1 | Beamforming, filtering, and low-latency compute target | Core high-priority integration | Central technical milestone, not a stretch add-on |
| Antenna array | Active GNSS L1/L2 patch antennas | 5 | Coherent array inputs | In integration | Final selected model should be recorded once fixed |
| RF cabling | U.FL-to-SMA coax cables | 5 | Front-end interconnect from array path to SDR | In integration | Verify connector gender, length, and loss |
| RF cabling | SMA-to-SMA coax jumpers | 5 | Clean routing between modules | In integration | Keep matched lengths where required |
| Mechanical | Ground plane / rigid plate | 1 | Stable antenna mounting surface | In progress | Aluminum plate is the current assumption |
| Mechanical | Standoffs, fasteners, spacers | Assorted | Mounting, spacing, and strain relief | In progress | Record exact sizes once selected |
| Power | Pi 5 power supply | 1 | Host power | Required | Record voltage/current rating |
| Power | Portable battery or external DC source | 1 | Portable field operation | Pending selection | Add only after current draw is measured |

## Procurement notes
- Freeze the exact antenna model before ordering any redundant cabling.
- Prefer matched cable lengths within the antenna array path unless measurements show mismatch is acceptable after calibration.
- Record vendor, part number, unit price, and lead time once the list is finalized.

## Next updates needed
- Replace placeholder antenna wording with exact manufacturer and part number.
- Add unit cost, vendor, and ordered/not-ordered state.
- Split any optional accessories into a separate deferred BOM.
