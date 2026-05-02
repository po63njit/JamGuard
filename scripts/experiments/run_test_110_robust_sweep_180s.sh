#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
cd "$REPO_ROOT"
if [[ -f .venv/bin/activate ]]; then source .venv/bin/activate; fi

RUN_NAME="${RUN_NAME:-test_110}"
CAPTURE_DIR="${CAPTURE_DIR:-/media/patryk/X31/test_110}"
FS="${FS:-2400000}"
MAX_SAMPLES="${MAX_SAMPLES:-432000000}"
PROC_ROOT="${PROC_ROOT:-/media/patryk/X31/jamguard_processed_test110}"
CONF_TEMPLATE="${CONF_TEMPLATE:-/media/patryk/X31/test_110/test_110/ch0.conf}"

JAMMER_KINDS_STR="${JAMMER_KINDS_STR:-cw chirp wideband_noise}"
AMPS_STR="${AMPS_STR:-3 8 16}"
KEEP_CFILES="${KEEP_CFILES:-0}"
RESET_SUMMARY="${RESET_SUMMARY:-1}"

SUMMARY="${SUMMARY:-results/tables/test_110_robust_sweep_180s.csv}"
LOG_ROOT="${LOG_ROOT:-results/logs/test_110_robust_sweep_180s}"
RUN_ROOT="$HOME/gnss_sdr_runs/test_110_robust_sweep_180s"

mkdir -p "$PROC_ROOT" "$LOG_ROOT" "$RUN_ROOT" results/tables

if [[ "$RESET_SUMMARY" == "1" ]]; then
  rm -f "$SUMMARY"
fi

set_conf_kv() {
  local file="$1"
  local key="$2"
  local val="$3"
  if grep -q "^${key}=" "$file"; then
    sed -i "s|^${key}=.*|${key}=${val}|" "$file"
  else
    echo "${key}=${val}" >> "$file"
  fi
}

run_gnss() {
  local conf="$1"
  local log="$2"

  # Prevent GNSS-SDR from blocking forever when the jammed case has no acquisition.
  set_conf_kv "$conf" "Acquisition_1C.blocking" "false"
  set_conf_kv "$conf" "Acquisition_1C.max_dwells" "1"
  set_conf_kv "$conf" "SignalSource.repeat" "false"
  set_conf_kv "$conf" "SignalSource.enable_throttle_control" "false"

  local timeout_s="${GNSS_TIMEOUT_S:-90s}"

  set +e
  timeout -s KILL "$timeout_s" stdbuf -oL -eL gnss-sdr --config_file="$conf" 2>&1 | tee "$log"
  local code=${PIPESTATUS[0]}
  set -e

  echo "gnss_sdr_exit_code=$code" | tee -a "$log"
  return 0
}

echo "=== Ensuring 180s phase-aligned input exists ==="
if [[ ! -f "$PROC_ROOT/${RUN_NAME}_phase_180s/ch0.cfile" ]]; then
  python scripts/analysis/phase_align_channels.py \
    --input-dir "$CAPTURE_DIR" \
    --output-dir "$PROC_ROOT/${RUN_NAME}_phase_180s" \
    --channels 5 \
    --pattern 'ch{}.cfile' \
    --max-samples "$MAX_SAMPLES" \
    --force
fi

echo "=== Raw CH0 180s baseline ==="
RAW_DIR="$RUN_ROOT/raw_ch0_180s"
mkdir -p "$RAW_DIR"
RAW_CONF="$RAW_DIR/raw_ch0_180s.conf"
RAW_LOG="$RAW_DIR/raw_ch0_180s_gnss_sdr.log"

if [[ ! -f "$RAW_LOG" ]]; then
  cp "$CONF_TEMPLATE" "$RAW_CONF"
  set_conf_kv "$RAW_CONF" "SignalSource.filename" "$CAPTURE_DIR/ch0.cfile"
  set_conf_kv "$RAW_CONF" "SignalSource.samples" "$MAX_SAMPLES"
  set_conf_kv "$RAW_CONF" "SignalSource.repeat" "false"
  set_conf_kv "$RAW_CONF" "SignalSource.enable_throttle_control" "false"
  run_gnss "$RAW_CONF" "$RAW_LOG"
fi

cp "$RAW_LOG" "$LOG_ROOT/" || true

python scripts/reports/parse_gnss_sdr_log.py \
  --case-id "${RUN_NAME}_raw_ch0_180s" \
  --jammer-kind "none" \
  --amplitude "0" \
  --branch "raw_ch0" \
  --log "$RAW_LOG" \
  --out-csv "$SUMMARY"

read -r -a JAMMER_KINDS <<< "$JAMMER_KINDS_STR"
read -r -a AMPS <<< "$AMPS_STR"

for kind in "${JAMMER_KINDS[@]}"; do
  for amp in "${AMPS[@]}"; do
    amp_tag="${amp//./p}"
    case_id="${RUN_NAME}_${kind}_amp${amp_tag}_180s"

    echo
    echo "============================================================"
    echo "CASE: $case_id"
    echo "============================================================"

    synth_dir="$PROC_ROOT/${case_id}_synth"
    lcmv_dir="$PROC_ROOT/${case_id}_lcmv"
    case_run_dir="$RUN_ROOT/$case_id"
    mkdir -p "$case_run_dir"

    echo "=== Injecting $kind jammer, amp=$amp ==="
    python scripts/beamforming/inject_parametric_jammer.py \
      --input-dir "$PROC_ROOT/${RUN_NAME}_phase_180s" \
      --output-dir "$synth_dir" \
      --sample-rate "$FS" \
      --channels 5 \
      --pattern 'ch{}.cfile' \
      --max-samples "$MAX_SAMPLES" \
      --kind "$kind" \
      --amplitude "$amp" \
      --force

    echo "=== Running LCMV nuller ==="
    python scripts/beamforming/run_lcmv_nuller.py \
      --input-dir "$synth_dir" \
      --output-dir "$lcmv_dir" \
      --metrics-csv "results/tables/${case_id}_lcmv_metrics.csv" \
      --sample-rate "$FS" \
      --channels 5 \
      --pattern 'ch{}.cfile' \
      --max-samples "$MAX_SAMPLES" \
      --force

    echo "=== Skipping GNSS-SDR on jammed CH0 ==="
    jam_conf="$case_run_dir/${case_id}_jammed_ch0.conf"
    jam_log="$case_run_dir/${case_id}_jammed_ch0_gnss_sdr.log"
    cp "$CONF_TEMPLATE" "$jam_conf"
    set_conf_kv "$jam_conf" "SignalSource.filename" "$synth_dir/ch0.cfile"
    set_conf_kv "$jam_conf" "SignalSource.samples" "0"
    set_conf_kv "$jam_conf" "SignalSource.repeat" "false"
    set_conf_kv "$jam_conf" "SignalSource.enable_throttle_control" "false"
    {
      echo "GNSS-SDR skipped for jammed CH0."
      echo "Reason: strong jammed single-channel acquisition can block GNSS-SDR."
      echo "Use spectral/JNR metrics for jammed baseline; use GNSS-SDR metrics for LCMV recovery."
    } | tee "$jam_log"

    python scripts/reports/parse_gnss_sdr_log.py \
      --case-id "$case_id" \
      --jammer-kind "$kind" \
      --amplitude "$amp" \
      --branch "jammed_ch0" \
      --log "$jam_log" \
      --out-csv "$SUMMARY"

    echo "=== Skipping GNSS-SDR on LCMV output inside sweep ==="
    lcmv_conf="$case_run_dir/${case_id}_lcmv.conf"
    lcmv_log="$case_run_dir/${case_id}_lcmv_gnss_sdr.log"
    cp "$CONF_TEMPLATE" "$lcmv_conf"
    set_conf_kv "$lcmv_conf" "SignalSource.filename" "$lcmv_dir/lcmv_ch0ref_null.cfile"
    set_conf_kv "$lcmv_conf" "SignalSource.samples" "0"
    set_conf_kv "$lcmv_conf" "SignalSource.repeat" "false"
    set_conf_kv "$lcmv_conf" "SignalSource.enable_throttle_control" "false"
    {
      echo "GNSS-SDR skipped for LCMV output inside robust sweep."
      echo "Reason: batch GNSS-SDR can block on some cases."
      echo "Run GNSS-SDR manually afterward on selected LCMV outputs."
    } | tee "$lcmv_log"

    python scripts/reports/parse_gnss_sdr_log.py \
      --case-id "$case_id" \
      --jammer-kind "$kind" \
      --amplitude "$amp" \
      --branch "lcmv" \
      --log "$lcmv_log" \
      --out-csv "$SUMMARY"

    cp "$jam_log" "$lcmv_log" "$LOG_ROOT/" || true

    if [[ "$KEEP_CFILES" == "0" ]]; then
      echo "=== Removing large intermediate cfiles for this case ==="
      rm -rf "$synth_dir" "$lcmv_dir"
    fi
  done
done

echo
echo "DONE. Summary CSV:"
echo "$SUMMARY"
