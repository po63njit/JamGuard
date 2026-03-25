# Capture Metadata Template

Use one metadata file per capture session.

```yaml
capture_id: ""
date: ""
operator: ""
location: ""
mode: ""
prototype_revision: ""
antenna_geometry_revision: ""
host_configuration_ref: ""
fpga_configuration_ref: ""
krakensdr_status: ""
sample_rate: ""
center_frequency: ""
channels_used: 5
raw_data_storage_path: ""
notes: ""
quick_observations:
  - ""
```

## Rule
The metadata file should exist before or at the same time as the raw capture, not days later.
