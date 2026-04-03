# JamGuard MVP Overview

JamGuard MVP is an offline analysis application for coherent KrakenSDR capture sets.

## Implemented now
- CF32 one-file-per-channel loading with validation
- Channel power/RMS ranking and summary table
- PSD estimation and plotting (Welch)
- Cross-channel correlation matrix + lag + relative phase estimates
- Relative complex gain calibration with JSON save/load
- UCA geometry and azimuth steering vectors
- Fixed delay-and-sum beamforming
- Synthetic directional tone interferer injection
- End-to-end anti-jam demo pipeline with saved plots + JSON summary

## Deferred (explicitly)
- Adaptive MVDR/LCMV null steering
- Real-time streaming capture integration
- GUI/dashboard

MVP target: produce capstone-ready evidence quickly from real simultaneous 5-channel recordings.
