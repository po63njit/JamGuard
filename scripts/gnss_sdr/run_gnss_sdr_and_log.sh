#!/usr/bin/env bash
set -euo pipefail
CONF="$1"; LOG="${2:-$(basename "${CONF%.conf}")_gnss_sdr.log}"
gnss-sdr --config_file="$CONF" 2>&1 | tee "$LOG"
