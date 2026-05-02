# FILE: README.md

# JamGuard / COTS Anti-Jamming GNSS Beamforming System

This repository documents and organizes the senior capstone software workflow for a low-cost COTS anti-jamming GNSS beamforming prototype.

The project evolved from an early wearable concept into a portable multi-antenna GNSS anti-jam prototype built around:

- 5-element active GNSS antenna array
- KrakenSDR coherent 5-channel RF front end
- Raspberry Pi 5 host for capture, logging, orchestration, and field operation
- Ubuntu desktop/laptop analysis environment for GNSS-SDR and Python processing
- Offline Python beamforming, calibration, jammer injection, nulling, and report packaging
- PolarFire SoC FPGA platform as the intended acceleration path for deterministic beamforming/filtering kernels

## Main workflows

1. Hardware bring-up and capture
2. GNSS-SDR validation of raw and processed captures
3. Channel sanity checks and IQ file validation
4. Multi-channel coherence and phase-alignment analysis
5. Synthetic interferer injection
6. LCMV/MVDR-style anti-jam beamforming/nulling
7. GNSS-SDR validation after nulling
8. Results packaging for report/presentation
9. Indoor conducted RF test-bench operation
10. Outdoor real-GNSS + conducted jammer data collection
11. FPGA handoff: fixed-point test vectors and kernel partitioning

## Recommended repository layout

```text
jamguard/
├── README.md
├── docs/
│   ├── 00_project_context.md
│   ├── 01_capture_pathway.md
│   ├── 02_gnss_sdr_validation.md
│   ├── 03_signal_analysis_pathway.md
│   ├── 04_jammer_injection_and_nulling.md
│   ├── 05_results_packaging.md
│   ├── 06_rf_testbench_and_field_testing.md
│   ├── 07_fpga_handoff.md
│   └── 08_common_functions.md
├── src/
│   └── jamguard/
│       ├── io/
│       ├── dsp/
│       ├── gnss/
│       ├── plotting/
│       ├── reports/
│       └── fpga/
├── scripts/
│   ├── capture/
│   ├── gnss_sdr/
│   ├── analysis/
│   ├── beamforming/
│   ├── reports/
│   └── fpga/
├── configs/
│   ├── krakensdr/
│   ├── gnss_sdr/
│   └── testbench/
├── notebooks/
├── tests/
├── data/
│   ├── raw/          # ignored by git
│   ├── processed/    # ignored by git
│   └── metadata/
└── results/
    ├── figures/
    ├── tables/
    └── logs/
```

## Important data policy

Do not commit large `.cfile`, `.bin`, `.sigmf-data`, GNSS-SDR logs, generated plots, or test captures directly into Git unless they are tiny examples. Store full captures on external SSD or local lab storage and commit only manifests, scripts, configs, and summarized metrics.


---

# FILE: docs/00_project_context.md

# 00 Project Context

## Purpose

The project demonstrates that a low-cost, mostly COTS, multi-antenna GNSS receiver can capture coherent multi-channel data and apply offline anti-jam beamforming techniques that are normally associated with much more expensive controlled-reception-pattern antenna systems.

## Final system framing

Use the general name:

**COTS Anti-Jamming GNSS Beamforming System**

Avoid using the earlier project name as the main title in final public-facing documents unless needed historically.

## Core architecture

```text
5x active GNSS antennas
        ↓
5-channel coherent KrakenSDR
        ↓
Raspberry Pi 5 capture/control host
        ↓
raw coherent IQ files
        ↓
Ubuntu analysis workstation / laptop
        ↓
Python validation + beamforming + nulling
        ↓
GNSS-SDR validation and report metrics
        ↓
future FPGA acceleration on PolarFire SoC
```

## Actual project accomplishments to preserve in docs

The project history indicates the following major accomplishments:

- Raspberry Pi 5 + KrakenSDR bring-up completed.
- KrakenSDR web/control path and data acquisition pipeline verified.
- 5-channel coherent captures recorded.
- Real GNSS L1 captures tested with GNSS-SDR.
- GNSS-SDR successfully tracked real GPS L1 C/A from previous recordings.
- Python analysis verified:
  - channel file validity
  - per-channel power sanity
  - coherence/timing checks
  - multi-window stability
  - data-driven phase alignment
  - synthetic interferer injection
  - jammer-aware nulling
- Representative coherence/timing result from a validated run:
  - `max_abs_lag_samples = 0`
  - timing stability classified as excellent
  - cross-window similarity classified as good
- Representative phase alignment metric from a validated run:
  - before alignment: about `0.094484`
  - after alignment: about `0.178319`
- A processed anti-jam output file was generated for GNSS-SDR validation using a filename pattern similar to:
  - `lcmv_ch0ref_null.cfile`

## Main datasets mentioned in project history

Use these as examples in documentation. Actual paths may differ.

```text
~/jamguard_analysis/test_106_preservation/
~/gnss_validation/test_111/
~/gnss_sdr_runs/outsidejam_001/
~/gnss_sdr_runs/outsidejam_001/outsidejam_001_ch0.conf
~/gnss_sdr_runs/outsidejam_001/outsidejam_001_lcmv_antijam.conf
/media/patryk/X31/outsidejam_001_antijam/lcmv_ch0ref_null.cfile
```

## Development principle

Every script should do one of four jobs:

1. Capture or preserve raw data.
2. Validate that the raw data is structurally and physically plausible.
3. Produce a processed artifact that can be defended with metrics.
4. Package evidence into tables, figures, logs, and reproducible configs.


---

# FILE: docs/01_capture_pathway.md

# 01 Capture Pathway

This document covers the Raspberry Pi 5 + KrakenSDR capture path and the scripts used to initialize, verify, record, and preserve coherent 5-channel IQ data.

## Hardware context

Typical field capture setup:

```text
5 active GNSS antennas
    ↓
KrakenSDR CH0..CH4
    ↓
Raspberry Pi 5 running KrakenSDR software / Heimdall DAQ
    ↓
external SSD or local capture folder
    ↓
five synchronized complex IQ channel files
```

Typical channel files:

```text
ch0.cfile
ch1.cfile
ch2.cfile
ch3.cfile
ch4.cfile
```

Expected format:

- complex64 / GNU Radio `gr_complex`
- interleaved float32 I, float32 Q
- one file per KrakenSDR channel
- same sample rate across all files
- same sample count, or close enough to trim safely to common length

## Script: `heimdall_only_start.sh`

### Role

Starts the KrakenSDR Heimdall DAQ backend without necessarily running the full direction-finding UI stack.

### Project context

In the project chat, the start/stop helper scripts were copied from the KrakenSDR source tree into the top-level KrakenSDR working directory:

```bash
cd ~/krakensdr
cp gr-krakensdr/heimdall_only_start.sh .
cp gr-krakensdr/heimdall_only_stop.sh .
chmod +x heimdall_only_start.sh heimdall_only_stop.sh
```

### Typical use

```bash
cd ~/krakensdr
./heimdall_only_stop.sh
./heimdall_only_start.sh
```

### What to document in the repo

- Source path of the helper script.
- KrakenSDR image/version used.
- Raspberry Pi OS image used.
- Whether the system autostarts the KrakenSDR stack on boot.
- Whether the script is run before or after bias-tee activation.

## Script: `enable_kraken_biastee.sh`

### Role

Enables the KrakenSDR bias tee lines used to power active GNSS antennas.

### Important warning

The exact control method depends on the KrakenSDR software image and driver setup. In the project, the practical goal was to enable bias tee on the Raspberry Pi 5 before recording real GNSS data from active antennas.

KrakenSDR uses GPIO-controlled bias tee behavior that is not identical to a single normal RTL-SDR Blog V3 dongle. A robust repo script should therefore:

1. Check that KrakenSDR devices are visible.
2. Stop acquisition before changing bias settings.
3. Enable the required bias tee GPIOs.
4. Restart acquisition.
5. Optionally verify current draw or LNA power if measurement equipment is available.

### Conservative script template

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "[JamGuard] Stopping Heimdall before bias tee changes..."
cd "$HOME/krakensdr"
./heimdall_only_stop.sh || true

echo "[JamGuard] Listing RTL devices..."
rtl_test -t || true

echo "[JamGuard] Enabling KrakenSDR bias tee GPIO lines."
echo "Verify GPIO numbering on the installed KrakenSDR image before relying on this script."

for gpio in 1 2 3 4 5; do
    echo "Enabling bias tee GPIO ${gpio}"
    rtl_biast -d 0 -g "${gpio}" -b 1 || {
        echo "Failed on GPIO ${gpio}; check rtl_biast version and KrakenSDR driver."
        exit 1
    }
done

echo "[JamGuard] Restarting Heimdall..."
./heimdall_only_start.sh
```

### Validation

After enabling bias tee:

- Active GNSS antennas should power correctly.
- Noise floor should change compared with unpowered antennas.
- GNSS-SDR should eventually show acquisition/tracking improvement in outdoor conditions.
- The KrakenSDR should remain synchronized.

## Script: `record_5ch_capture.sh`

### Role

Creates a timestamped folder and records all five KrakenSDR channels to `.cfile` outputs using the chosen GNU Radio Companion flowgraph or capture command.

### Inputs

- Run name, such as `test_106`, `outsidejam_001`, or `baseline_001`.
- Sample rate, commonly `2048000` samples/s or `2400000` samples/s depending on config.
- Capture duration, such as 20 s, 60 s, or 600 s.
- Output directory, preferably external SSD.

### Recommended behavior

```bash
#!/usr/bin/env bash
set -euo pipefail

RUN_NAME="${1:-test_$(date +%Y%m%d_%H%M%S)}"
FS="${FS:-2048000}"
DURATION="${DURATION:-60}"
OUT_ROOT="${OUT_ROOT:-$HOME/gnss_validation}"
OUT_DIR="${OUT_ROOT}/${RUN_NAME}"

mkdir -p "$OUT_DIR"

cat > "$OUT_DIR/capture_manifest.json" <<EOF
{
  "run_name": "${RUN_NAME}",
  "sample_rate_sps": ${FS},
  "duration_s": ${DURATION},
  "channels": 5,
  "format": "complex64_interleaved_float32",
  "created_local": "$(date -Iseconds)",
  "notes": "Fill in antenna geometry, weather, location class, and test mode."
}
EOF

echo "[JamGuard] Start your GNU Radio/KrakenSDR recorder flowgraph now."
echo "[JamGuard] Expected outputs:"
echo "  ${OUT_DIR}/ch0.cfile"
echo "  ${OUT_DIR}/ch1.cfile"
echo "  ${OUT_DIR}/ch2.cfile"
echo "  ${OUT_DIR}/ch3.cfile"
echo "  ${OUT_DIR}/ch4.cfile"
```

## Script: `check_capture_files.py`

### Role

Checks that all five channel files exist, have valid sizes, and contain complex64 samples.

### Command

```bash
python scripts/analysis/check_capture_files.py   --input-dir ~/gnss_validation/test_106   --sample-rate 2048000   --channels 5
```

### Outputs

- Per-channel file size
- Per-channel sample count
- Capture duration inferred from samples
- Whether all channel lengths match
- Recommended trim length

### Implementation notes

The script should:

- Reject files whose byte size is not divisible by 8.
- Warn if channel file sizes differ.
- Report duration as `samples / sample_rate`.
- Create `capture_file_check.csv`.

## Common capture failures and interpretations

| Symptom | Likely cause | Action |
|---|---|---|
| One channel file missing | GNU Radio sink path wrong or channel disabled | Check flowgraph paths and channel indices |
| File size not divisible by 8 | Incomplete/corrupted complex64 file | Discard or trim only if corruption is at end |
| One channel much lower power | Cable/antenna/LNA/bias issue | Swap cable/antenna and rerun |
| One channel saturated | Gain too high or strong interference | Lower gain or check source level |
| Files differ in length | Capture stopped unevenly | Trim all channels to minimum length |
| GNSS-SDR never acquires | Indoor capture, weak GNSS, bad center frequency, wrong sample rate | Move outside, verify config, check spectrum |


---

# FILE: docs/02_gnss_sdr_validation.md

# 02 GNSS-SDR Validation Pathway

This document covers the scripts and configuration pattern used to validate raw and processed captures with GNSS-SDR.

## Purpose

GNSS-SDR is used as an independent downstream receiver to show that the captured or beamformed IQ stream still contains usable GPS L1 C/A signal content.

For this project, GNSS-SDR validation is important because it makes the anti-jam result more defensible than only showing internal DSP metrics.

## Primary command pattern

The project repeatedly used this pattern:

```bash
gnss-sdr --config_file=<config>.conf 2>&1 | tee <run_name>_gnss_sdr.log
```

Example from project history:

```bash
cd ~/gnss_sdr_runs/outsidejam_001

cp outsidejam_001_ch0.conf outsidejam_001_lcmv_antijam.conf

sed -i 's|^SignalSource.filename=.*|SignalSource.filename=/media/patryk/X31/outsidejam_001_antijam/lcmv_ch0ref_null.cfile|' outsidejam_001_lcmv_antijam.conf

gnss-sdr --config_file=outsidejam_001_lcmv_antijam.conf 2>&1 | tee outsidejam_001_lcmv_antijam_gnss_sdr.log
```

## Script: `make_gnss_sdr_config.py`

### Role

Generates a GNSS-SDR `.conf` file for a selected `.cfile`.

### Inputs

- IQ file path
- Sample rate
- Output config path
- Number of GPS L1 C/A channels
- Optional internal sampling frequency

### Example command

```bash
python scripts/gnss_sdr/make_gnss_sdr_config.py   --iq-file /media/patryk/X31/outsidejam_001_antijam/lcmv_ch0ref_null.cfile   --sample-rate 2048000   --channels-1c 8   --output configs/gnss_sdr/outsidejam_001_lcmv_antijam.conf
```

### Important config fields

```ini
[GNSS-SDR]

GNSS-SDR.internal_fs_sps=2048000

SignalSource.implementation=File_Signal_Source
SignalSource.filename=/path/to/input.cfile
SignalSource.item_type=gr_complex
SignalSource.sampling_frequency=2048000
SignalSource.samples=0
SignalSource.repeat=false
SignalSource.enable_throttle_control=false

SignalConditioner.implementation=Signal_Conditioner
DataTypeAdapter.implementation=Pass_Through
DataTypeAdapter.item_type=gr_complex
InputFilter.implementation=Pass_Through
InputFilter.item_type=gr_complex
Resampler.implementation=Pass_Through
Resampler.item_type=gr_complex

Channels_1C.count=8
Channels.in_acquisition=8
```

## Script: `update_gnss_sdr_input.sh`

### Role

Copies a known-working GNSS-SDR config and replaces only the input filename.

### Example

```bash
#!/usr/bin/env bash
set -euo pipefail

BASE_CONF="$1"
NEW_IQ="$2"
OUT_CONF="$3"

cp "$BASE_CONF" "$OUT_CONF"
sed -i "s|^SignalSource.filename=.*|SignalSource.filename=${NEW_IQ}|" "$OUT_CONF"

echo "Created $OUT_CONF"
grep '^SignalSource.filename=' "$OUT_CONF"
```

### Use case

Use this when comparing:

- raw channel 0
- phase-aligned channel 0 reference
- delay-and-sum output
- LCMV/MVDR nulling output

## Script: `run_gnss_sdr_and_log.sh`

### Role

Runs GNSS-SDR and stores logs consistently.

### Example

```bash
#!/usr/bin/env bash
set -euo pipefail

CONF="$1"
LOG="${2:-$(basename "${CONF%.conf}")_gnss_sdr.log}"

gnss-sdr --config_file="$CONF" 2>&1 | tee "$LOG"
```

## Script: `parse_gnss_sdr_log.py`

### Role

Extracts GNSS-SDR performance evidence from logs.

### Recommended metrics

- Run start/end time if present
- Number of acquisition attempts
- PRNs acquired
- PRNs tracked
- Tracking lock events
- C/N0 values if printed
- PVT solution status if available
- Error or warning counts
- Whether a navigation solution was achieved
- Total run duration

### Example command

```bash
python scripts/gnss_sdr/parse_gnss_sdr_log.py   --log logs/outsidejam_001_lcmv_antijam_gnss_sdr.log   --output results/tables/outsidejam_001_lcmv_gnss_sdr_summary.csv
```

## GNSS-SDR validation comparison table

| Case | Input | Processing | Expected evidence |
|---|---|---|---|
| Raw CH0 | `ch0.cfile` | None | Baseline tracking/acquisition |
| Raw CH1..CH4 | `ch*.cfile` | None | Channel-by-channel health |
| Phase aligned | `aligned_ch0ref.cfile` | Phase alignment | Shows cleaned/combined output is still valid |
| Null output | `lcmv_ch0ref_null.cfile` | Anti-jam nulling | Should improve jammer-bin metric and ideally preserve GNSS-SDR tracking |
| Jammed raw | `jammed_ch0.cfile` | Synthetic/controlled jammer | Shows degraded baseline |
| Anti-jam | `lcmv_ch0ref_null.cfile` | Null steering | Shows suppression and recovered tracking metric |


---

# FILE: docs/03_signal_analysis_pathway.md

# 03 Signal Analysis Pathway

This document covers the most commonly used Python analysis scripts for raw 5-channel KrakenSDR captures.

## Overall analysis chain

```text
five raw channel files
        ↓
file structure check
        ↓
channel power and spectrum check
        ↓
sample-lag/timing coherence check
        ↓
multi-window coherence stability
        ↓
phase alignment to reference channel
        ↓
optional synthetic jammer injection
        ↓
beamforming/nulling
        ↓
metrics + plots + processed cfile
```

## Script: `inspect_cfile.py`

### Role

Loads one `.cfile` and prints basic information.

### Command

```bash
python scripts/analysis/inspect_cfile.py   --input ~/gnss_validation/test_106/ch0.cfile   --sample-rate 2048000
```

### Output

```text
file: ch0.cfile
bytes: ...
complex64 samples: ...
duration_s: ...
mean_i: ...
mean_q: ...
rms: ...
power_dbfs: ...
nan_count: 0
inf_count: 0
```

## Script: `channel_health_summary.py`

### Role

Checks all five files and creates a health table.

### Command

```bash
python scripts/analysis/channel_health_summary.py   --input-dir ~/gnss_validation/test_106   --sample-rate 2048000   --output results/tables/test_106_channel_health.csv
```

### Metrics

- Sample count
- Duration
- Mean I/Q
- RMS
- Power in dBFS
- Peak magnitude
- Clipping indicator
- NaN/Inf count
- Relative channel power

## Script: `plot_psd.py`

### Role

Creates per-channel FFT or Welch PSD plots.

### Command

```bash
python scripts/analysis/plot_psd.py   --input-dir ~/gnss_validation/test_106   --sample-rate 2048000   --center-frequency 1575420000   --output results/figures/test_106_psd.png
```

## Script: `coarse_sample_lag_check.py`

### Role

Estimates integer-sample lag between channels by cross-correlation.

### Command

```bash
python scripts/analysis/coarse_sample_lag_check.py   --input-dir ~/jamguard_analysis/test_106_preservation   --reference-channel 0   --max-samples 2000000   --output results/tables/test_106_lag_check.csv
```

### Important project result

A validated project run showed:

```text
max_abs_lag_samples = 0
timing stability = EXCELLENT
```

This is a key result because beamforming assumes channels are time-aligned well enough that phase alignment and covariance methods are meaningful.

## Script: `multi_window_coherence.py`

### Role

Checks whether timing/coherence remains stable across multiple time windows instead of only at the beginning of a file.

### Command

```bash
python scripts/analysis/multi_window_coherence.py   --input-dir ~/jamguard_analysis/test_106_preservation   --sample-rate 2048000   --reference-channel 0   --window-samples 262144   --num-windows 8   --output results/tables/test_106_multi_window_coherence.csv
```

### Metrics

- Window index
- Start sample
- Pairwise lag relative to CH0
- Pairwise normalized correlation
- Phase estimate relative to CH0
- Cross-window similarity
- Stability classification

## Script: `phase_align_channels.py`

### Role

Computes complex phase correction factors so all channels are aligned to a reference channel.

### Command

```bash
python scripts/analysis/phase_align_channels.py   --input-dir ~/jamguard_analysis/test_106_preservation   --reference-channel 0   --sample-rate 2048000   --output-dir results/processed/test_106_phase_aligned   --metrics results/tables/test_106_phase_alignment.csv
```

### Important project result

One validated analysis pass improved the coherence-style metric approximately from:

```text
before = 0.094484
after  = 0.178319
```

Do not overclaim this as absolute GNSS improvement. Document it as a signal-processing consistency metric showing that data-driven phase alignment increased channel agreement.

## Script: `export_calibration_json.py`

### Role

Exports calibration factors for repeatable downstream use.

### Output example

```json
{
  "run_name": "test_106",
  "reference_channel": 0,
  "sample_rate_sps": 2048000,
  "phase_corrections": [
    {"channel": 0, "real": 1.0, "imag": 0.0},
    {"channel": 1, "real": 0.91, "imag": -0.41},
    {"channel": 2, "real": 0.30, "imag": 0.95},
    {"channel": 3, "real": -0.72, "imag": 0.69},
    {"channel": 4, "real": -0.15, "imag": -0.99}
  ]
}
```

## Common analysis functions

- `read_complex64_cfile(path, count=None, offset=0)`
- `write_complex64_cfile(path, x)`
- `load_multichannel_cfiles(input_dir, pattern="ch{}.cfile", channels=5)`
- `trim_to_common_length(channels)`
- `compute_power_dbfs(x)`
- `estimate_sample_lag(x_ref, x)`
- `phase_align_to_ref(X, ref_ch=0)`
- `compute_covariance_matrix(X)`
- `plot_psd(x, fs, fc=None)`


---

# FILE: docs/04_jammer_injection_and_nulling.md

# 04 Jammer Injection and Nulling Pathway

This document covers synthetic jammer injection and anti-jam beamforming/nulling.

## Safety boundary

All jammer-related work must remain inside one of these safe modes:

1. Offline synthetic injection into recorded IQ files.
2. Conducted wired RF test bench with attenuation, combiners, terminators, and shielding.
3. Playback of already-recorded data into software only.

Do not radiate a GNSS jammer over the air. GNSS interference can disrupt safety-critical navigation and is illegal in many jurisdictions.

## Conceptual processing chain

```text
real 5-channel GNSS capture
        ↓
calibrate/phase-align channels
        ↓
inject synthetic spatial interferer OR record conducted interferer
        ↓
estimate covariance / jammer direction signature
        ↓
compute anti-jam weights
        ↓
apply weights across channels
        ↓
write single-channel beamformed output
        ↓
validate with PSD metrics and GNSS-SDR
```

## Script: `inject_synthetic_jammer.py`

### Role

Adds a controlled synthetic interferer to existing multi-channel IQ files to test nulling algorithms without radiating.

### Inputs

- Clean 5-channel capture
- Sample rate
- Interferer type:
  - tone
  - chirp
  - band-limited noise
- Relative jammer-to-signal/noise level
- Spatial signature:
  - fixed complex phase vector
  - uniform circular array steering vector
  - manually supplied per-channel phase offsets

### Command

```bash
python scripts/beamforming/inject_synthetic_jammer.py   --input-dir ~/jamguard_analysis/test_106_preservation   --output-dir results/processed/test_106_synth_jam   --sample-rate 2048000   --jammer-type tone   --jammer-offset-hz 250000   --relative-level-db 25   --array-radius-m 0.08   --azimuth-deg 70
```

## Script: `estimate_jammer_bin.py`

### Role

Finds the dominant interference bin or band in a capture.

### Command

```bash
python scripts/beamforming/estimate_jammer_bin.py   --input-dir results/processed/test_106_synth_jam   --sample-rate 2048000   --output results/tables/test_106_jammer_bin.csv
```

## Script: `run_lcmv_nuller.py`

### Role

Applies a linearly constrained minimum variance or null-steering style beamformer to suppress a jammer while preserving a reference/look direction.

### Command

```bash
python scripts/beamforming/run_lcmv_nuller.py   --input-dir results/processed/test_106_synth_jam   --sample-rate 2048000   --reference-channel 0   --array-radius-m 0.08   --look-azimuth-deg 0   --null-azimuth-deg 70   --output-cfile results/processed/test_106_lcmv/lcmv_ch0ref_null.cfile   --metrics results/tables/test_106_lcmv_metrics.csv
```

### Output file naming

The project history used a clear and useful naming pattern:

```text
lcmv_ch0ref_null.cfile
```

Keep this naming convention because it documents:

- algorithm: LCMV
- reference: channel 0
- purpose: nulling output

## Script: `compare_nulling_metrics.py`

### Role

Compares raw, jammed, and anti-jam outputs.

### Command

```bash
python scripts/beamforming/compare_nulling_metrics.py   --raw results/processed/test_106_synth_jam/ch0.cfile   --processed results/processed/test_106_lcmv/lcmv_ch0ref_null.cfile   --sample-rate 2048000   --jammer-offset-hz 250000   --output results/tables/test_106_nulling_comparison.csv
```

### Recommended metrics

| Metric | Meaning |
|---|---|
| `jammer_bin_power_before_db` | Interference bin before nulling |
| `jammer_bin_power_after_db` | Interference bin after nulling |
| `suppression_db` | Before minus after |
| `noise_floor_before_db` | Local noise estimate before |
| `noise_floor_after_db` | Local noise estimate after |
| `output_rms_dbfs` | Ensures output is not invalid/silent |
| `weight_norm` | Detects unstable beamformer weights |
| `condition_number` | Detects covariance instability |

## Script: `run_antijam_gnss_sdr_validation.sh`

### Role

Runs GNSS-SDR on the anti-jam output and logs the result.

### Example based on project history

```bash
cd ~/gnss_sdr_runs/outsidejam_001

cp outsidejam_001_ch0.conf outsidejam_001_lcmv_antijam.conf

sed -i 's|^SignalSource.filename=.*|SignalSource.filename=/media/patryk/X31/outsidejam_001_antijam/lcmv_ch0ref_null.cfile|' outsidejam_001_lcmv_antijam.conf

gnss-sdr --config_file=outsidejam_001_lcmv_antijam.conf 2>&1 | tee outsidejam_001_lcmv_antijam_gnss_sdr.log
```

## Common beamforming functions

- `steering_vector_uca(num_elements, radius_m, azimuth_deg, wavelength_m)`
- `estimate_covariance(X, diagonal_loading=1e-3)`
- `mvdr_weights(R, a_look)`
- `lcmv_weights(R, constraint_matrix, response_vector)`
- `null_steering_weights(a_look, a_null)`
- `apply_beamformer(X, w)`
- `jammer_bin_power(x, fs, offset_hz, rbw_hz)`

## Claims that are safe to make

Good:

- “The script reduced the selected interference bin by X dB.”
- “The processed output remained structurally valid complex64 IQ.”
- “GNSS-SDR was run on the processed output to evaluate whether GPS L1 C/A tracking was preserved or recovered.”
- “The result is an offline validation of the beamforming method using coherent COTS receiver data.”

Avoid unless proven with strong data:

- “The system fully prevents GNSS jamming.”
- “The prototype matches military CRPA performance.”
- “The array provides production-grade navigation integrity.”
- “The FPGA real-time path is complete” unless actually completed.


---

# FILE: docs/05_results_packaging.md

# 05 Results Packaging Pathway

This document covers scripts that turn raw logs, CSV metrics, figures, and GNSS-SDR results into report-ready evidence.

## Purpose

The final report and presentation need clean, defensible evidence. The project should preserve:

- capture metadata
- channel health tables
- coherence/timing tables
- phase-alignment tables
- nulling suppression metrics
- GNSS-SDR validation tables
- figures showing spectra and results
- a final master results table

## Script: `make_master_results_table.py`

### Role

Combines all run-level metrics into one table.

### Command

```bash
python scripts/reports/make_master_results_table.py   --run-dir results   --output results/tables/master_results_table.csv
```

### Recommended columns

| Column | Meaning |
|---|---|
| `run_name` | Test identifier |
| `date` | Capture or analysis date |
| `mode` | indoor, outdoor, synthetic, conducted, playback |
| `sample_rate_sps` | Sample rate |
| `duration_s` | Capture duration |
| `channels_valid` | True/false |
| `max_abs_lag_samples` | Worst sample lag |
| `timing_class` | Excellent/good/problem |
| `phase_metric_before` | Pre-alignment channel agreement |
| `phase_metric_after` | Post-alignment channel agreement |
| `jammer_type` | none, synthetic tone, conducted tone, etc. |
| `suppression_db` | Jammer suppression |
| `gnss_raw_tracked_prns` | Raw GNSS-SDR tracked PRNs |
| `gnss_antijam_tracked_prns` | Processed GNSS-SDR tracked PRNs |
| `notes` | Manual notes |

## Script: `plot_results_summary.py`

### Role

Creates final report figures.

### Recommended plots

1. Per-channel PSD before processing.
2. Per-channel power bar chart.
3. Multi-window coherence stability plot.
4. Phase alignment before/after plot.
5. Jammer spectrum before/after nulling.
6. GNSS-SDR acquisition/tracking comparison.
7. System block diagram, usually generated separately as a diagram.

## Script: `generate_report_appendix.py`

### Role

Creates a Markdown appendix with commands, script descriptions, and file references.

### Command

```bash
python scripts/reports/generate_report_appendix.py   --results-dir results   --output docs/generated_appendix_script_log.md
```

## Suggested final-report table

| Test | Purpose | Input | Processing | Main metric | Result |
|---|---|---|---|---|---|
| Channel file validation | Prove capture files are usable | CH0-CH4 `.cfile` | File/format check | file size/sample count | pass/fail |
| Channel power check | Detect bad RF path | CH0-CH4 `.cfile` | RMS/PSD | relative dBFS | pass/fail |
| Coarse timing check | Verify coherent capture | CH0-CH4 `.cfile` | cross-correlation | max lag samples | e.g. 0 samples |
| Multi-window coherence | Verify stability | full capture | windowed correlation | stability class | excellent/good |
| Phase alignment | Improve array agreement | full capture | complex phase correction | metric before/after | improved |
| Synthetic jammer test | Controlled anti-jam validation | clean capture | add interferer | JNR/offset | generated |
| LCMV nulling | Suppress jammer | jammed capture | beamforming | suppression dB | measured |
| GNSS-SDR raw | Navigation validation | raw CH0 | GNSS-SDR | PRNs/tracking/CN0 | measured |
| GNSS-SDR anti-jam | Navigation validation | null output | GNSS-SDR | PRNs/tracking/CN0 | measured |

## Report-safe language

Use measured language:

- “The project demonstrated offline adaptive/null-steering processing on coherent five-channel COTS SDR captures.”
- “The validated captures showed sample-level timing alignment across channels.”
- “The beamforming output was exported as a GNSS-SDR-compatible complex64 file.”
- “GNSS-SDR logs were used to evaluate whether the processed output preserved GPS L1 C/A usability.”

Do not overstate field readiness without final outdoor dataset metrics.


---

# FILE: docs/06_rf_testbench_and_field_testing.md

# 06 RF Test Bench and Field Testing Pathway

This document covers the indoor conducted RF test bench and outdoor real-GNSS data-collection setup.

## Safety and legality

GNSS jamming must not be radiated over the air.

Allowed project modes:

- Offline synthetic jammer injection into IQ recordings.
- Conducted RF testing through coax, attenuation, splitters, combiners, DC blocks, and 50-ohm terminations.
- Shielded testing where leakage is controlled.
- Playback-only software demos.

Not allowed:

- Connecting a jammer signal to an antenna and radiating it outdoors or indoors.
- Testing without attenuation/termination.
- Transmitting near GNSS L1 in a way that can leak into the environment.

## Indoor conducted test bench

### Concept

```text
bladeRF TX0 synthetic GNSS path
    → attenuator chain
    → splitter
    → five equal branches
    → combiner input A for CH0..CH4

bladeRF TX1 synthetic jammer path
    → attenuator chain
    → optional extra attenuation
    → splitter
    → five branches
    → DC block per branch if needed
    → combiner input B for CH0..CH4

combiner outputs
    → KrakenSDR CH0..CH4
```

### Why this matters

The indoor conducted test bench lets the project create repeatable jammer conditions without radiating. This is the best controlled method for report-quality suppression metrics.

## Script: `testbench_manifest.py`

### Role

Creates a test-bench configuration manifest so the wiring state is documented.

### Example command

```bash
python scripts/reports/testbench_manifest.py   --run-name indoor_wired_001   --gnss-source bladeRF_TX0   --jammer-source bladeRF_TX1   --sample-rate 2048000   --output results/metadata/indoor_wired_001_manifest.json
```

## Outdoor real-GNSS + conducted jammer setup

### Concept

```text
5 active GNSS antennas
    → combiner input A on each channel path

conducted jammer/reference branch
    → attenuation
    → splitter
    → DC blocks as needed
    → combiner input B on each channel path

combiner outputs
    → KrakenSDR CH0..CH4
```

### Bias tee concern

Active GNSS antennas need DC power. The RF wiring must allow bias tee DC to reach the antenna branch while preventing DC from feeding back into the jammer/source path. In practice:

- Put DC blocks on the conducted jammer branch where needed.
- Verify whether the combiner passes DC on the antenna side.
- Do not assume all combiners pass bias tee DC.
- Measure DC carefully before connecting expensive devices.
- Verify active antenna power with a multimeter or known LNA response if possible.

## Script: `field_run_checklist.md`

This should be a documentation file, not executable code.

### Pre-run checklist

- KrakenSDR powered.
- Raspberry Pi 5 powered from stable supply.
- External SSD mounted and writable.
- Bias tee enabled if using active antennas.
- Antenna array physically stable.
- Antenna geometry photographed.
- Cable mapping CH0..CH4 documented.
- GNSS-SDR config sample rate known.
- Run manifest created.
- No RF jammer signal radiating.
- All conducted RF paths attenuated/terminated.

### During run

- Record start time.
- Record duration.
- Save screenshots of KrakenSDR status if useful.
- Watch for overflows or dropped samples.
- Confirm files are growing.
- Avoid moving the array mid-capture.

### Post-run

- Stop capture cleanly.
- Run file-size check.
- Copy configs and logs into run folder.
- Add run notes immediately.
- Preserve raw files before processing.

## Script: `preserve_run.sh`

### Role

Copies raw data, configs, and logs into an immutable run folder.

### Example

```bash
#!/usr/bin/env bash
set -euo pipefail

SRC="$1"
DEST="$2"

mkdir -p "$DEST/raw" "$DEST/configs" "$DEST/logs" "$DEST/metadata"

cp "$SRC"/*.cfile "$DEST/raw/"
cp "$SRC"/*.conf "$DEST/configs/" 2>/dev/null || true
cp "$SRC"/*.log "$DEST/logs/" 2>/dev/null || true
cp "$SRC"/*.json "$DEST/metadata/" 2>/dev/null || true

sha256sum "$DEST/raw"/*.cfile > "$DEST/metadata/raw_sha256.txt"

echo "Preserved run at $DEST"
```

## Outdoor run names

Use clear naming:

```text
outside_baseline_001
outsidejam_001
outsidejam_001_antijam
outsidejam_001_lcmv_antijam
```

## What to include in report

- One photo of the physical 5-element antenna array.
- One block diagram of outdoor/indoor setup.
- A table of cable lengths and channel mapping.
- A safety note that jammer validation was synthetic or conducted, not radiated.
- Capture sample rate and duration.
- GNSS-SDR raw vs processed result.


---

# FILE: docs/07_fpga_handoff.md

# 07 FPGA Handoff Pathway

This document covers the software-to-FPGA handoff path for the PolarFire SoC platform.

## Goal

The FPGA path should not start by trying to run the whole GNSS receiver on the FPGA. The correct first step is to export small, verified DSP kernels and compare fixed-point FPGA outputs against Python golden references.

## Candidate FPGA kernels

Start with these in order:

1. Complex multiply/accumulate for beamforming weights.
2. Per-channel phase correction.
3. Covariance accumulation over a block.
4. Power/energy estimator.
5. FIR/notch filtering if needed.
6. Weight application using precomputed host-side weights.
7. Later: weight solving or adaptive update logic.

## Script: `export_fpga_test_vectors.py`

### Role

Exports small blocks of complex IQ data and expected Python outputs for FPGA simulation.

### Command

```bash
python scripts/fpga/export_fpga_test_vectors.py   --input-dir ~/jamguard_analysis/test_106_preservation   --weights results/processed/test_106_lcmv/weights.json   --sample-count 4096   --q-format q1.15   --output-dir fpga/test_vectors/test_106_lcmv
```

### Outputs

```text
x_ch0_q15.hex
x_ch1_q15.hex
x_ch2_q15.hex
x_ch3_q15.hex
x_ch4_q15.hex
weights_q15.hex
expected_output_q15.hex
metadata.json
```

## Script: `compare_fpga_output.py`

### Role

Compares FPGA simulation or hardware output against Python golden output.

### Command

```bash
python scripts/fpga/compare_fpga_output.py   --expected fpga/test_vectors/test_106_lcmv/expected_output_q15.hex   --actual fpga/output/test_106_lcmv_output.hex   --q-format q1.15   --output results/tables/test_106_fpga_compare.csv
```

### Metrics

- Mean absolute error
- Max absolute error
- RMS error
- Saturation count
- Correlation with floating-point output
- Pass/fail threshold

## Script: `quantize_weights.py`

### Role

Converts floating-point complex weights into fixed-point values.

### Command

```bash
python scripts/fpga/quantize_weights.py   --weights results/processed/test_106_lcmv/weights.json   --q-format q1.15   --output fpga/test_vectors/test_106_lcmv/weights_q15.hex
```

## Suggested FPGA documentation section

### Python reference

- NumPy complex64 or complex128 model.
- Floating-point weights.
- Output `.cfile`.

### Fixed-point model

- Chosen Q format.
- Saturation behavior.
- Rounding behavior.
- Error relative to Python.

### HDL kernel

- Inputs: 5 complex samples per clock group or stream.
- Coefficients: 5 complex weights.
- Output: one complex beamformed sample.
- Operation:
  - complex multiply each input by conjugate weight
  - sum five products
  - scale/round/saturate
  - stream output

### Validation

Use the same test vector in:

1. Python float model
2. Python fixed-point model
3. HDL simulation
4. FPGA hardware if available

## Safe final-report framing

If FPGA work is partial, describe it as:

> The project established a clear FPGA acceleration path by identifying the beamforming multiply-accumulate operation as the first hardware kernel and preparing Python-generated test vectors for fixed-point comparison. Full real-time FPGA integration remains future work unless hardware validation is completed.

If FPGA output is validated, describe it as:

> The FPGA kernel reproduced the Python fixed-point beamforming reference within the selected error tolerance on exported multi-channel IQ test vectors.


---

# FILE: docs/08_common_functions.md

# 08 Common Functions and APIs

This document defines the common functions that should exist in the Python package so the project does not become a collection of disconnected one-off scripts.

## Package layout

```text
src/jamguard/
├── io/
│   ├── cfile.py
│   └── manifest.py
├── dsp/
│   ├── metrics.py
│   ├── coherence.py
│   ├── calibration.py
│   ├── beamforming.py
│   └── jammer.py
├── gnss/
│   ├── config.py
│   └── logs.py
├── plotting/
│   ├── spectra.py
│   └── report_figures.py
├── reports/
│   ├── tables.py
│   └── appendix.py
└── fpga/
    ├── fixed_point.py
    └── vectors.py
```

## `jamguard.io.cfile`

Required functions:

```python
read_complex64_cfile(path, count=None, offset=0)
write_complex64_cfile(path, x)
cfile_sample_count(path)
load_5ch_capture(input_dir, pattern="ch{}.cfile", channels=5, count=None)
trim_to_common_length(arrays)
```

Purpose:

- Load GNU Radio complex64 `.cfile` data.
- Validate byte size.
- Trim channels to common length.
- Avoid silent corruption.

## `jamguard.dsp.metrics`

Required functions:

```python
rms(x)
power_dbfs(x, eps=1e-12)
peak_mag(x)
count_invalid(x)
summarize_channel(x, fs)
```

## `jamguard.dsp.coherence`

Required functions:

```python
normalized_xcorr_lag(x_ref, x, max_lag)
windowed_lag_analysis(X, fs, window_samples, hop_samples, ref_ch=0)
coherence_score(X, ref_ch=0)
```

## `jamguard.dsp.calibration`

Required functions:

```python
estimate_phase_correction(x_ref, x)
estimate_all_phase_corrections(X, ref_ch=0)
apply_phase_corrections(X, corrections)
```

## `jamguard.dsp.jammer`

Required functions:

```python
generate_tone_jammer(num_samples, fs, offset_hz, amplitude, phase=0)
generate_chirp_jammer(num_samples, fs, f0_hz, f1_hz, amplitude)
inject_spatial_interferer(X, jammer, spatial_signature)
estimate_dominant_bin(x, fs)
```

## `jamguard.dsp.beamforming`

Required functions:

```python
wavelength(freq_hz, c=299792458.0)
uca_positions(num_elements, radius_m)
steering_vector_uca(num_elements, radius_m, azimuth_deg, freq_hz)
covariance_matrix(X, diagonal_loading=0.0)
mvdr_weights(R, a_look)
lcmv_weights(R, C, f)
apply_weights(X, w)
```

## `jamguard.gnss.config`

Required functions:

```python
make_file_signal_source_config(iq_file, fs, channels_1c=8)
replace_signal_source_filename(config_text, new_filename)
```

## `jamguard.gnss.logs`

Required functions:

```python
parse_gnss_sdr_log(path)
summarize_gnss_sdr_runs(log_paths)
```

## `jamguard.fpga.fixed_point`

Required functions:

```python
quantize_complex(x, q_format)
dequantize_complex(iq, q_format)
write_hex_vector(path, values)
read_hex_vector(path, q_format)
```

## CLI standards

Every script should:

- use `argparse`
- print clear input/output paths
- fail loudly on missing files
- write machine-readable CSV/JSON outputs
- not overwrite raw captures unless `--force` is passed
- save parameters in a manifest
- work from absolute or relative paths
- avoid hardcoded `/home/patryk/...` paths except in examples

## Test standards

At minimum, create tests for:

- complex64 read/write round trip
- sample count detection
- phase correction on known synthetic phase offset
- steering vector dimensions
- beamformer output shape
- GNSS-SDR config filename replacement
- log parser on a small fixture log


---

# FILE: CODEX_REPO_PROMPT.md

# CODEX Prompt: Create or Update the JamGuard GitHub Repository

You are Codex acting as a senior Python/DSP/GNSS/FPGA repository engineer. Create or update my GitHub repository for my senior capstone project.

## Project name

Use the general public-facing name:

**COTS Anti-Jamming GNSS Beamforming System**

Historical/internal name: **JamGuard**

## Project context

This project is a low-cost COTS anti-jamming GNSS beamforming prototype. It uses:

- 5-element active GNSS antenna array
- KrakenSDR coherent 5-channel receiver
- Raspberry Pi 5 for capture, logging, orchestration, and field operation
- Ubuntu desktop/laptop for offline analysis
- GNSS-SDR for downstream GPS L1 C/A validation
- Python/NumPy/SciPy for coherence checks, phase alignment, synthetic jammer injection, and nulling
- PolarFire SoC FPGA as the future acceleration target for deterministic beamforming/filtering kernels

The project has already completed:

- Raspberry Pi 5 + KrakenSDR bring-up
- KrakenSDR capture pipeline verification
- 5-channel coherent captures
- GNSS-SDR validation on real GPS L1 C/A recordings
- offline Python checks for channel health, timing/coherence, phase alignment, synthetic interferer injection, and jammer-aware nulling
- generation of an anti-jam output file using a naming pattern like `lcmv_ch0ref_null.cfile`
- GNSS-SDR config editing and execution with commands like:
  `gnss-sdr --config_file=<config>.conf 2>&1 | tee <log>.log`

Representative validated metrics from project history:

- `max_abs_lag_samples = 0`
- timing stability classified as excellent
- cross-window similarity classified as good
- phase alignment metric improved from about `0.094484` to `0.178319`

## Your job

Create or update the repository so it becomes a clean, reproducible, report-ready engineering project. Do not delete existing working scripts. Refactor only if safe. If something already exists, improve it while preserving compatibility.

## Required repository layout

Create this structure if missing:

```text
jamguard/
├── README.md
├── docs/
│   ├── 00_project_context.md
│   ├── 01_capture_pathway.md
│   ├── 02_gnss_sdr_validation.md
│   ├── 03_signal_analysis_pathway.md
│   ├── 04_jammer_injection_and_nulling.md
│   ├── 05_results_packaging.md
│   ├── 06_rf_testbench_and_field_testing.md
│   ├── 07_fpga_handoff.md
│   └── 08_common_functions.md
├── src/
│   └── jamguard/
│       ├── __init__.py
│       ├── io/
│       ├── dsp/
│       ├── gnss/
│       ├── plotting/
│       ├── reports/
│       └── fpga/
├── scripts/
│   ├── capture/
│   ├── gnss_sdr/
│   ├── analysis/
│   ├── beamforming/
│   ├── reports/
│   └── fpga/
├── configs/
│   ├── krakensdr/
│   ├── gnss_sdr/
│   └── testbench/
├── tests/
├── results/
│   ├── figures/
│   ├── tables/
│   └── logs/
├── data/
│   ├── raw/
│   ├── processed/
│   └── metadata/
├── pyproject.toml
├── requirements.txt
└── .gitignore
```

## Data policy

Do not commit large IQ data files. Add these to `.gitignore`:

```gitignore
*.cfile
*.sigmf-data
*.bin
*.iq
*.raw
*.wav
*.log
data/raw/
data/processed/
results/figures/
results/logs/
__pycache__/
.venv/
```

Keep small example fixtures only under `tests/fixtures/`.

## Implement the Python package

Create these modules and functions.

### `src/jamguard/io/cfile.py`

Implement:

- `read_complex64_cfile(path, count=None, offset=0)`
- `write_complex64_cfile(path, x)`
- `cfile_sample_count(path)`
- `load_multichannel_capture(input_dir, pattern="ch{}.cfile", channels=5, count=None)`
- `trim_to_common_length(arrays)`

Requirements:

- GNU Radio `gr_complex` format: interleaved float32 I/Q, one complex64 vector.
- Validate byte size divisible by 8.
- Use pathlib.
- Raise useful exceptions.

### `src/jamguard/dsp/metrics.py`

Implement:

- `rms(x)`
- `power_dbfs(x, eps=1e-12)`
- `peak_mag(x)`
- `count_invalid(x)`
- `summarize_channel(x, fs)`

### `src/jamguard/dsp/coherence.py`

Implement:

- `normalized_xcorr_lag(x_ref, x, max_lag)`
- `windowed_lag_analysis(X, fs, window_samples, hop_samples, ref_ch=0)`
- `coherence_score(X, ref_ch=0)`

### `src/jamguard/dsp/calibration.py`

Implement:

- `estimate_phase_correction(x_ref, x)`
- `estimate_all_phase_corrections(X, ref_ch=0)`
- `apply_phase_corrections(X, corrections)`

### `src/jamguard/dsp/jammer.py`

Implement:

- `generate_tone_jammer(num_samples, fs, offset_hz, amplitude, phase=0.0)`
- `generate_chirp_jammer(num_samples, fs, f0_hz, f1_hz, amplitude)`
- `inject_spatial_interferer(X, jammer, spatial_signature)`
- `estimate_dominant_bin(x, fs)`

### `src/jamguard/dsp/beamforming.py`

Implement:

- `wavelength(freq_hz, c=299792458.0)`
- `uca_positions(num_elements, radius_m)`
- `steering_vector_uca(num_elements, radius_m, azimuth_deg, freq_hz)`
- `covariance_matrix(X, diagonal_loading=0.0)`
- `mvdr_weights(R, a_look)`
- `lcmv_weights(R, C, f)`
- `apply_weights(X, w)`

Use stable numerical methods. Add diagonal loading where appropriate.

### `src/jamguard/gnss/config.py`

Implement:

- `make_file_signal_source_config(iq_file, fs, channels_1c=8)`
- `replace_signal_source_filename(config_text, new_filename)`

Generate GNSS-SDR configs for complex64 file input.

### `src/jamguard/gnss/logs.py`

Implement a robust parser:

- `parse_gnss_sdr_log(path)`
- `summarize_gnss_sdr_runs(log_paths)`

Extract acquisition/tracking/CN0/PVT evidence when present. Do not fail if a field is missing; return `None` or empty lists.

### `src/jamguard/fpga/fixed_point.py`

Implement:

- `quantize_complex(x, q_format="q1.15")`
- `dequantize_complex(iq, q_format="q1.15")`
- `write_hex_vector(path, values)`
- `read_hex_vector(path, q_format="q1.15")`

## Create CLI scripts

All scripts must use `argparse`, print input/output paths, and write CSV/JSON outputs.

### Capture / utility scripts

- `scripts/capture/check_kraken_devices.sh`
- `scripts/capture/enable_kraken_biastee.sh`
- `scripts/capture/preserve_run.sh`

The bias-tee script must include a warning that GPIO numbering depends on KrakenSDR software image/driver version and should be verified before use.

### GNSS-SDR scripts

- `scripts/gnss_sdr/make_gnss_sdr_config.py`
- `scripts/gnss_sdr/update_gnss_sdr_input.sh`
- `scripts/gnss_sdr/run_gnss_sdr_and_log.sh`
- `scripts/gnss_sdr/parse_gnss_sdr_log.py`

### Analysis scripts

- `scripts/analysis/check_capture_files.py`
- `scripts/analysis/inspect_cfile.py`
- `scripts/analysis/channel_health_summary.py`
- `scripts/analysis/plot_psd.py`
- `scripts/analysis/coarse_sample_lag_check.py`
- `scripts/analysis/multi_window_coherence.py`
- `scripts/analysis/phase_align_channels.py`
- `scripts/analysis/export_calibration_json.py`

### Beamforming scripts

- `scripts/beamforming/inject_synthetic_jammer.py`
- `scripts/beamforming/estimate_jammer_bin.py`
- `scripts/beamforming/run_lcmv_nuller.py`
- `scripts/beamforming/compare_nulling_metrics.py`

### Report scripts

- `scripts/reports/make_master_results_table.py`
- `scripts/reports/plot_results_summary.py`
- `scripts/reports/generate_report_appendix.py`
- `scripts/reports/export_figures_for_report.py`

### FPGA scripts

- `scripts/fpga/export_fpga_test_vectors.py`
- `scripts/fpga/quantize_weights.py`
- `scripts/fpga/compare_fpga_output.py`

## Documentation requirements

Create or update the docs folder using the documentation topics below:

1. Project context and architecture.
2. Raspberry Pi 5 + KrakenSDR capture workflow.
3. GNSS-SDR validation workflow.
4. Signal analysis workflow.
5. Synthetic jammer injection and nulling workflow.
6. Results packaging workflow.
7. RF test bench and field testing workflow.
8. FPGA handoff workflow.
9. Common functions/API reference.

Use the wording from this prompt. Keep the docs practical and command-driven.

## Safety wording

Add a safety section stating:

- GNSS jammer work must remain offline synthetic or conducted through shielded/attenuated RF paths.
- Do not radiate GNSS interference.
- Use DC blocks, attenuators, terminations, and shielding in conducted tests.
- Preserve raw captures and label all processed outputs clearly.

## Tests

Create pytest tests for:

- complex64 cfile read/write round trip
- sample count detection
- phase correction on known synthetic phase shift
- steering vector output dimensions
- beamformer output shape
- GNSS-SDR config filename replacement
- fixed-point quantize/dequantize sanity

## README requirements

The README should include:

- project overview
- architecture diagram in text
- quickstart install
- how to run channel validation
- how to run coherence analysis
- how to run synthetic jammer injection
- how to run LCMV nulling
- how to run GNSS-SDR validation
- how to create the master results table
- safety/legal warning
- data management warning

## Coding style

- Python 3.10+
- NumPy, SciPy, pandas, matplotlib
- No hardcoded `/home/patryk` paths except in docs examples
- Use type hints where reasonable
- Keep raw data out of git
- Write clear docstrings
- Prefer small functions over large scripts
- Make every CLI output reproducible

## Final deliverable from Codex

After modifying the repo, summarize:

1. Files created.
2. Files changed.
3. Scripts added.
4. Tests added.
5. Any assumptions made.
6. Exact commands I should run next.
