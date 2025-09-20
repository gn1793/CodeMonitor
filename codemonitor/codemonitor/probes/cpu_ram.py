from typing import Dict
import os

def _bytes_to_mb(n: float) -> float:
    return round(n / (1024 * 1024), 3)

def probe() -> Dict:
    # psutil import is here to allow package import even if psutil missing
    try:
        import psutil
    except Exception:
        return {
            "cpu": {"total_pct": 0.0, "proc_pct": 0.0},
            "ram": {"pct": 0.0, "used_mb": 0.0, "avail_mb": 0.0,
                    "proc_rss_mb": 0.0, "proc_vms_mb": 0.0},
        }

    cpu_total = psutil.cpu_percent(interval=None)
    proc_pct = 0.0
    try:
        p = psutil.Process(os.getpid())
        proc_pct = p.cpu_percent(interval=None) / psutil.cpu_count(logical=True)
    except Exception:
        pass

    vm = psutil.virtual_memory()
    rss = vms = 0.0
    try:
        p = psutil.Process(os.getpid())
        m = p.memory_info()
        rss = _bytes_to_mb(m.rss)
        vms = _bytes_to_mb(m.vms)
    except Exception:
        pass

    return {
        "cpu": {"total_pct": float(cpu_total), "proc_pct": float(proc_pct)},
        "ram": {"pct": float(vm.percent),
                "used_mb": _bytes_to_mb(vm.used),
                "avail_mb": _bytes_to_mb(vm.available),
                "proc_rss_mb": rss,
                "proc_vms_mb": vms},
    }
