# Metrics Definition

These metrics should be used consistently across host-only and host-plus-FPGA comparisons.

| Metric | What it indicates | Notes |
|---|---|---|
| Channel health | Whether all channels are usable | Baseline gating metric |
| Coherence stability | Repeatability of channel relationships over time | Needed before credible beamforming |
| Suppression benefit | Measured interference reduction or improvement in signal quality | Final demo metric |
| Latency | Processing delay through the pipeline | Important for FPGA value |
| Runtime / throughput | How much data can be processed per unit time | Compare host-only versus hybrid |
| Power draw | Portability and practical deployment constraint | Add when instrumentation is available |

## Rule
Do not change metric definitions mid-stream without logging the reason in project management notes.
