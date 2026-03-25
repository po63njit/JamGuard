# Beamforming Partition Plan

## Goal
Keep the FPGA central to the design while sequencing the work so baseline validation happens first.

## Partitioning principle
The Raspberry Pi should remain the supervisory and logging host. The PolarFire SoC should own the timing-critical and highly parallel signal-processing work once coherent input data is validated.

## Proposed phase split
### Phase A: Host-only reference path
- validate coherent captures
- implement calibration checks
- establish delay-and-sum reference behavior
- define metrics and expected outputs

### Phase B: Hybrid partition design
- identify kernels with deterministic and parallel structure
- define data width, throughput, and latency requirements
- decide what must remain on host for flexibility

### Phase C: FPGA-centered execution path
- move selected kernels to PolarFire SoC
- retain Pi control, mode selection, logging, and result management
- compare host-only and hybrid execution on the same datasets

## Candidate FPGA kernels
- channel delay alignment
- weighted summation
- covariance or intermediate matrix accumulation
- FIR or narrowband filtering blocks
- real-time metric generation for health monitoring

## Candidate host responsibilities
- system bring-up
- UI and operator control
- session metadata
- result storage
- non-real-time analysis and plotting

## Success criteria
- FPGA contribution is measurable, not cosmetic.
- The host and FPGA paths produce comparable outputs on shared test cases.
- The final demo clearly shows the Pi as controller and the FPGA as major compute engine.
