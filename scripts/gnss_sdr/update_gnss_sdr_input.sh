#!/usr/bin/env bash
set -euo pipefail
BASE="$1"; IQ="$2"; OUT="$3"
cp "$BASE" "$OUT"
sed -i "s|^SignalSource.filename=.*|SignalSource.filename=$IQ|" "$OUT"
