# KrakenSDR Bring-Up Checklist

This checklist captures the known-good baseline for the Raspberry Pi 5 plus KrakenSDR host path.

## Objective
Confirm that the host platform and SDR front end are operational before array integration begins.

## Baseline setup
- Raspberry Pi 5 prepared with the KrakenRF Raspberry Pi image or equivalent validated host environment
- KrakenSDR connected and powered correctly
- Network access working for local UI and remote administration

## Bring-up checklist
- Boot Raspberry Pi 5 successfully
- Confirm network connectivity
- Confirm storage is mounted and has free space for logs
- Confirm KrakenSDR is detected by the host
- Open the KrakenSDR web interface
- Verify data acquisition pipeline starts without immediate fault
- Verify connection status is healthy
- Verify frame synchronization is healthy
- Verify sample-delay synchronization is healthy
- Verify IQ synchronization is healthy
- Verify power indicators are acceptable
- Record screenshots of the known-good state

## Evidence to save
- screenshot of web UI status
- software image or version used
- date and operator
- notes on any warnings or instability

## Exit condition
Do not proceed to array debugging or FPGA integration until the host and SDR baseline is repeatable on demand.
