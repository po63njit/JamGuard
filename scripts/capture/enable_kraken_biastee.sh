#!/usr/bin/env bash
set -euo pipefail
echo "WARNING: KrakenSDR bias-tee GPIO numbering depends on image/driver version. Verify before use."
for gpio in 1 2 3 4 5; do echo "Enable GPIO $gpio"; done
