# Architecture

## Core Data Model
- `CaptureMetadata`: experiment/capture-level metadata.
- `ChannelData`: one IQ stream plus channel attributes.
- `MultiChannelCapture`: synchronized channel collection + utility conversion.
- `CalibrationResult`, `BeamformingResult`, `AnalysisResult`: standardized result payloads.

## Module Boundaries
- `jamguard.io`: raw loading/parsing.
- `jamguard.data`: domain objects and dataset access.
- `jamguard.analysis`: diagnostics, correlation, phase/delay, synthetic scenarios.
- `jamguard.geometry`: array geometry primitives.
- `jamguard.beamforming`: steering vectors and beamforming algorithms.
- `jamguard.calibration`: channel mismatch estimation/correction.
- `jamguard.metrics`: performance metrics.
- `jamguard.plotting`: figure generation.
- `jamguard.reporting`: report and experiment logs.
- `jamguard.cli`: orchestration entrypoints.

## Design Principles
- Reproducible experiments via config + logging + structured outputs.
- Narrow interfaces between modules for easier FPGA cross-validation.
- Minimal but real implementations with TODOs at research-heavy seams.
