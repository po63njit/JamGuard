# Capture Workflow

## Goal
Standardize how coherent capture sessions are run so the resulting data is traceable and comparable.

## Workflow
1. Confirm the host and SDR match the latest known-good state.
2. Record prototype revision, antenna geometry revision, and cable set.
3. Start logging with a session identifier.
4. Save capture metadata before collecting data.
5. Run the capture.
6. Save quick-look observations immediately after capture.
7. Archive raw files outside Git and commit only metadata and summaries.

## Session identifier format
`YYYY-MM-DD_location_mode_revision_run`

Example:
`2026-03-25_labbench_baseline_P1_run01`
