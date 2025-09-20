from typing import List, Dict

def probe_all() -> List[Dict]:
    try:
        import pynvml
    except Exception:
        # nvidia-ml-py not installed or unavailable
        return []

    gpus = []
    try:
        pynvml.nvmlInit()
        count = pynvml.nvmlDeviceGetCount()
        for i in range(count):
            h = pynvml.nvmlDeviceGetHandleByIndex(i)
            name = pynvml.nvmlDeviceGetName(h).decode('utf-8', errors='ignore') if isinstance(pynvml.nvmlDeviceGetName(h), bytes) else str(pynvml.nvmlDeviceGetName(h))
            uuid = pynvml.nvmlDeviceGetUUID(h).decode('utf-8', errors='ignore') if hasattr(pynvml, "nvmlDeviceGetUUID") else ""
            util = pynvml.nvmlDeviceGetUtilizationRates(h)
            mem = pynvml.nvmlDeviceGetMemoryInfo(h)
            temp = 0.0
            power = 0.0
            try:
                temp = float(pynvml.nvmlDeviceGetTemperature(h, pynvml.NVML_TEMPERATURE_GPU))
            except Exception:
                pass
            try:
                power = float(pynvml.nvmlDeviceGetPowerUsage(h)) / 1000.0
            except Exception:
                pass

            gpus.append({
                "index": i,
                "name": name,
                "uuid": uuid,
                "util_pct": float(util.gpu),
                "mem_used_mb": round(mem.used / (1024*1024), 3),
                "mem_total_mb": round(mem.total / (1024*1024), 3),
                "power_w": power,
                "temp_c": temp,
            })
    except Exception:
        return []
    finally:
        try:
            pynvml.nvmlShutdown()
        except Exception:
            pass
    return gpus
