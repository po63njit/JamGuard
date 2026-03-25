# Repository Guide

## Where to put things
- Put course requirements and source templates in `docs/`.
- Put polished deliverables in `reports/`.
- Put source code and scripts in `software/`.
- Put mechanical, RF, and array design notes in `hardware/`.
- Put validation procedures and raw observations in `tests/`.
- Put milestones, risks, and meeting minutes in `project_management/`.

## Structure inside the major folders
- `docs/course_docs/`: instructor-provided or official reference material
- `docs/templates/`: reusable starting documents
- `hardware/antenna_array/`: geometry, dimensions, mounting, photos
- `hardware/bom/`: procurement-ready parts lists and substitutions
- `software/host/`: Pi setup, services, configs, small utilities
- `software/fpga/`: PolarFire docs, RTL, constraints, build scripts
- `software/algorithms/`: calibration, beamforming, analysis, notebooks
- `reports/figures/`: curated figures used in proposal/report/presentation assets
- `tests/bench/`: controlled procedures plus measured outputs
- `tests/field/`: outdoor validation procedures plus measured outputs

## Naming conventions
Use readable names with dates when useful:
- `2026-03-24_progress-report-draft.md`
- `array-spacing-v1.png`
- `krakensdr-bringup-notes.md`
- `pfsoc-beamforming-partition-plan.md`

## What should not be committed
- Raw SDR captures unless they are small and essential
- Vendor-generated FPGA build folders
- Temporary screenshots or duplicate exports
- Personal secrets, Wi-Fi credentials, tokens, or SSH keys

## Practical file rules
- Keep large raw data out of Git and store only metadata, summaries, and selected small excerpts here.
- Keep course templates and official documents unchanged; derive working drafts into `reports/`.
- Prefer one README per major subfolder so the next person knows what belongs there.
- When a folder has procedures and outputs, split them instead of mixing both in one directory.
