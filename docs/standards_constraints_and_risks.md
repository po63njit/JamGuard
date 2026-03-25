# Standards, Constraints, and Risks

This draft is intended to seed the ECE 414 proposal section on standards, constraints, risk, and uncertainty.

## Candidate relevant standards

### IEEE 802.3
Relevant for wired Ethernet networking between development systems, logging infrastructure, and any IP-based control path used in the prototype environment.

### IEEE 802.11
Relevant if the Raspberry Pi 5 host is operated over Wi-Fi during portable demonstrations or field logging.

### IEEE 754
Relevant to algorithm development and result reproducibility when floating-point processing is used in host-side calibration and beamforming reference code.

## Additional standards to investigate
- GNSS receiver and timing-related interface standards actually used by selected hardware
- EMC and lab safety guidance relevant to the bench environment
- board-vendor electrical and programming specifications for the PolarFire SoC platform

## Major constraint categories

### Technical constraints
- Coherence depends on stable channel behavior, geometry, and cable consistency.
- The SDR, host, and FPGA must exchange data with enough fidelity and timing discipline to preserve array usefulness.
- The prototype must remain portable without making the array mechanically unstable.

### Economic constraints
- The project should prioritize the core coherent-capture and FPGA path before optional accessories.
- Rework cost rises sharply if antennas, cabling, or mounts are changed late.
- Large, duplicated purchases should be avoided until the prototype 1 geometry is frozen.

### Legal, health, and safety constraints
- Testing must avoid creating harmful interference or unsafe RF practices.
- Power, cables, and mechanical mounting should be handled to reduce electrical and physical hazards.
- Lab and outdoor testing should follow applicable course and campus safety policies.

## Risk level definitions
| Level | Definition |
|---|---|
| Low | Unlikely to disrupt current milestone and easy to recover from within a few days |
| Moderate | Can delay a milestone or force rework, but there is a credible fallback path |
| High | Threatens the core demonstration path or invalidates major assumptions without a simple fallback |

## Current major risks
| Risk | Level | Why |
|---|---|---|
| Antenna geometry instability | High | Prevents credible coherent capture validation |
| Channel mismatch or failed path | High | Blocks calibration and beamforming progress |
| Pi to PolarFire integration friction | Moderate | Can delay FPGA milestone while host-only work continues |
| Incomplete test evidence | Moderate | Risks a weak final report even if the system partially works |
| Scope creep back into wearable features | Moderate | Diverts effort away from the validated technical core |
