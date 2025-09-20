from typing import Dict, Any, List
import socket
import os

SCHEMA_VERSION = "codemonitor/1.0"

def base_record(ts_ms: int, mark: str | None = None, extra: Dict[str, Any] | None = None) -> Dict[str, Any]:
    return {
        "schema": SCHEMA_VERSION,
        "ts_ms": ts_ms,
        "host": socket.gethostname(),
        "pid": os.getpid(),
        "proc_name": os.path.basename(getattr(os.sys, "argv", ["proc"])[0]),
        "mark": mark or "",
        "extra": extra or {},
    }

def flatten_record(rec: Dict[str, Any], max_gpus: int = 4) -> Dict[str, Any]:
    # Flatten to a CSV-friendly dict
    flat: Dict[str, Any] = {}
    keys = ["schema","ts_ms","host","pid","proc_name","mark"]
    for k in keys:
        flat[k] = rec.get(k, "")

    cpu = rec.get("cpu", {})
    flat["cpu_pct"] = cpu.get("total_pct", 0.0)
    flat["cpu_pct_proc"] = cpu.get("proc_pct", 0.0)

    ram = rec.get("ram", {})
    flat["ram_pct"] = ram.get("pct", 0.0)
    flat["ram_used_mb"] = ram.get("used_mb", 0.0)
    flat["ram_avail_mb"] = ram.get("avail_mb", 0.0)
    flat["proc_rss_mb"] = ram.get("proc_rss_mb", 0.0)
    flat["proc_vms_mb"] = ram.get("proc_vms_mb", 0.0)

    gpus: List[Dict[str, Any]] = rec.get("gpus", []) or []
    for i in range(max_gpus):
        g = gpus[i] if i < len(gpus) else {}
        flat[f"g{i}_util_pct"] = g.get("util_pct", 0.0)
        flat[f"g{i}_mem_used_mb"] = g.get("mem_used_mb", 0.0)
        flat[f"g{i}_mem_total_mb"] = g.get("mem_total_mb", 0.0)
        flat[f"g{i}_power_w"] = g.get("power_w", 0.0)
        flat[f"g{i}_temp_c"] = g.get("temp_c", 0.0)
        flat[f"g{i}_name"] = g.get("name", "")
        flat[f"g{i}_uuid"] = g.get("uuid", "")
    return flat
