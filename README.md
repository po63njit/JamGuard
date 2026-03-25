# JamGuard

Portable anti-jam GNSS receiver repository.

## Purpose
JamGuard is a portable multi-antenna anti-jam GNSS prototype built around:
- a 5-channel coherent KrakenSDR front end
- a Raspberry Pi 5 host controller
- a PolarFire SoC RISC-V/FPGA platform for acceleration

This repo is organized to support both course deliverables and the actual engineering build. The goal is to keep hardware notes, software artifacts, test evidence, and report material in one place without mixing drafts, generated files, and source material.

## Current scope
- **RF front end:** KrakenSDR, 5 coherent channels
- **Host platform:** Raspberry Pi 5
- **Acceleration platform:** PolarFire SoC Discovery Kit
- **Antenna system:** 5x active GNSS L1/L2 patch antennas
- **Prototype objective:** coherent capture, calibration, beamforming, and controlled anti-jam validation

## Repository layout
```text
JamGuard/
├── docs/                    # Course source docs, templates, overview, roadmap
├── hardware/                # Array geometry, BOM, RF/mechanical implementation
├── software/
│   ├── host/                # Pi setup, orchestration, configs, utilities
│   ├── fpga/                # PolarFire docs, RTL, scripts, constraints
│   ├── algorithms/          # Calibration, beamforming, analysis, notebooks
│   └── captures/            # Capture metadata only; raw data stays out of Git
├── reports/
│   ├── proposal/
│   ├── progress_reports/
│   ├── final_report/
│   └── figures/
├── tests/
│   ├── bench/               # Controlled bench procedures and results
│   └── field/               # Outdoor procedures and results
└── project_management/      # Milestones, risks, meetings, decisions, status
```

## Working rules
- Put source/reference documents in `docs/`.
- Put polished or submission-ready material in `reports/`.
- Put executable code, scripts, and machine-readable configs in `software/`.
- Put measurements, procedures, and evidence in `tests/`.
- Put planning, tradeoffs, and meeting logs in `project_management/`.
- Do not commit raw SDR captures, FPGA build folders, or large generated artifacts.

## Recommended next additions
1. Add an architecture/block diagram and interface map.
2. Add a real bill of materials with quantities, vendors, and status.
3. Add KrakenSDR bring-up notes with screenshots and known-good settings.
4. Add the first array geometry revision with physical dimensions and spacing rationale.
5. Add a host-side capture workflow and metadata format.
6. Add an FPGA partition plan showing what stays on the Pi and what moves to PolarFire.
7. Add at least one bench test procedure with explicit pass/fail criteria.

## Git setup
```bash
git init
git add .
git commit -m "Initial commit: JamGuard capstone repository"
```

To publish:
```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/JamGuard.git
git push -u origin main
```

## License
The scaffold currently uses MIT. Change it if course policy, sponsor requirements, or future commercialization plans require a different license.
