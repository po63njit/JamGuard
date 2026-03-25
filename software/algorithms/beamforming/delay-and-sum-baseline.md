# Delay-and-Sum Baseline

## Purpose
Define the first reference beamforming path before adaptive methods or FPGA offload are introduced.

## Why this baseline matters
- simple enough to validate against known expectations
- provides a comparison target for later FPGA work
- makes it easier to separate calibration issues from algorithm issues

## Required inputs
- synchronized multi-channel capture
- geometry description
- calibration constants

## Required outputs
- combined signal
- simple quality metrics
- traceable run metadata

## Acceptance target
This baseline should be working before MVDR or more advanced mitigation logic becomes a focus.
