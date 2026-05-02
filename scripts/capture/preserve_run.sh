#!/usr/bin/env bash
set -euo pipefail
SRC="$1"; DEST="$2"
mkdir -p "$DEST/raw" "$DEST/configs" "$DEST/logs" "$DEST/metadata"
cp "$SRC"/*.cfile "$DEST/raw/" 2>/dev/null || true
cp "$SRC"/*.conf "$DEST/configs/" 2>/dev/null || true
cp "$SRC"/*.log "$DEST/logs/" 2>/dev/null || true
