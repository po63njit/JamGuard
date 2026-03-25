# Risks

| Risk area | Example issue | Severity | Mitigation |
|---|---|---:|---|
| Coherence | channel mismatch or unstable phase | High | validate cables, shared references, and repeat calibration |
| Mechanical | antenna geometry inconsistency | High | use rigid mounting, documented spacing, repeatable cable routing |
| FPGA integration | slower-than-expected bring-up | Moderate | keep host-only reference chain working in parallel |
| RF environment | noisy or inconsistent test conditions | Moderate | prioritize bench and shielded/conducted tests |
| Schedule | documentation lag behind build progress | Moderate | commit notes and figures continuously |
