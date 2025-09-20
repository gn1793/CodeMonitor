import threading
import time
from typing import Dict, Any, List, Optional, Callable

from .utils.timeutil import now_ms
from .schema import base_record
from .probes import cpu_ram as cpu_probe
from .probes import nvidia as nvidia_probe

class Sampler(threading.Thread):
    def __init__(self, interval: float = 1.0,
                 write_fn: Optional[Callable[[Dict[str, Any]], None]] = None,
                 gpu: bool = True):
        super().__init__(daemon=True)
        self.interval = max(0.2, float(interval))
        self.write_fn = write_fn
        self.gpu = gpu
        self._stop = threading.Event()
        self._mark = None
        self._extra = None
        self._last_snapshot: Optional[Dict[str, Any]] = None

    def set_mark(self, tag: str, extra: Optional[Dict[str, Any]] = None):
        self._mark = tag
        self._extra = extra or {}

    def snapshot(self) -> Optional[Dict[str, Any]]:
        return self._last_snapshot

    def run(self):
        while not self._stop.is_set():
            ts = now_ms()
            rec = base_record(ts, mark=self._mark, extra=self._extra)
            rec.update(cpu_probe.probe())
            gpus = nvidia_probe.probe_all() if self.gpu else []
            rec["gpus"] = gpus
            self._last_snapshot = rec
            if self.write_fn:
                try:
                    self.write_fn(rec)
                except Exception:
                    pass
            time.sleep(self.interval)

    def stop(self):
        self._stop.set()
