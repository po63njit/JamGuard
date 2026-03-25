# Project Overview

## Project title
JamGuard: Portable Anti-Jam GNSS Receiver

## Summary
JamGuard is a portable multi-antenna anti-jam GNSS prototype that uses coherent multi-channel RF sampling, calibration, and beamforming to reduce the impact of interference while preserving navigation utility. The current implementation focus is a realistic portable bench/field prototype built around KrakenSDR, Raspberry Pi 5, and PolarFire SoC.

## Core engineering idea
1. Build a stable 5-antenna coherent capture path.
2. Validate array geometry, channel health, and calibration.
3. Implement reference beamforming and interference-mitigation flow.
4. Move timing-critical and highly parallel processing onto the FPGA / RISC-V platform.
5. Demonstrate measurable anti-jam benefit in controlled testing.

## Why this framing matters
The original wearable concept was ambitious, but the refined project framing keeps the novelty while making the implementation sequence more achievable for a one-person senior capstone.
