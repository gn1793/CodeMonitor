from typing import TypedDict, List, Dict, Optional, Any

class CpuInfo(TypedDict, total=False):
    total_pct: float
    proc_pct: float

class RamInfo(TypedDict, total=False):
    pct: float
    used_mb: float
    avail_mb: float
    proc_rss_mb: float
    proc_vms_mb: float

class GpuInfo(TypedDict, total=False):
    index: int
    name: str
    uuid: str
    util_pct: float
    mem_used_mb: float
    mem_total_mb: float
    power_w: float
    temp_c: float

class Snapshot(TypedDict, total=False):
    schema: str
    ts_ms: int
    host: str
    pid: int
    proc_name: str
    mark: str
    cpu: CpuInfo
    ram: RamInfo
    gpus: List[GpuInfo]
    extra: Dict[str, Any]
