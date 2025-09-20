# codemonitor

Low-overhead CPU/RAM/GPU monitor for long-running jobs (e.g., docking).

## Install

```bash
pip install git+https://github.com/<user>/codemonitor.git
# or with GPU extras (NVML):
pip install "codemonitor[gpu] @ git+https://github.com/<user>/codemonitor.git"
```

## Quick start

```python
from codemonitor import Monitor

with Monitor(sample_interval=1.0,
             sinks=["csv","jsonl"],
             out_dir="data/sysstats",
             gpu=True).running() as mon:
    mon.mark("warmup_done")
    # ... your workload ...
    snap = mon.snapshot()
    print("CPU:", snap["cpu"]["total_pct"], "RAM:", snap["ram"]["pct"])
```

Outputs CSV and/or JSONL under `out_dir`. If NVML is not available, GPU fields are omitted.
