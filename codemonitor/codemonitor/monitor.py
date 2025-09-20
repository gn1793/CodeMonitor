from __future__ import annotations
from pathlib import Path
from typing import Optional, Dict, Any, List

from .sampler import Sampler
from .sinks.csv_sink import CsvSink
from .sinks.jsonl_sink import JsonlSink
from .utils.env import get_env_interval, get_env_outdir

class Monitor:
    def __init__(self,
                 sample_interval: float = 1.0,
                 sinks: Optional[List[str]] = None,
                 out_dir: str | Path = "codemonitor_out",
                 gpu: bool = True,
                 max_gpus_for_csv: int = 4):
        self.sample_interval = get_env_interval(sample_interval)
        self.out_dir = Path(get_env_outdir(str(out_dir)))
        self.gpu = gpu
        self.max_gpus_for_csv = max_gpus_for_csv

        self._sinks: List[object] = []
        sinks = sinks or ["csv"]
        for s in sinks:
            if s == "csv":
                self._sinks.append(CsvSink(self.out_dir, max_gpus=self.max_gpus_for_csv))
            elif s == "jsonl":
                self._sinks.append(JsonlSink(self.out_dir))
            else:
                raise ValueError(f"Unknown sink: {s}")

        def write_fn(rec: Dict[str, Any]):
            for sk in self._sinks:
                sk.write(rec)

        self._sampler = Sampler(interval=self.sample_interval, write_fn=write_fn, gpu=self.gpu)

    # Public API
    def start(self) -> "Monitor":
        self._sampler.start()
        return self

    def stop(self) -> None:
        self._sampler.stop()
        for s in self._sinks:
            try:
                s.close()
            except Exception:
                pass

    def mark(self, tag: str, extra: Optional[Dict[str, Any]] = None) -> None:
        self._sampler.set_mark(tag, extra)

    def snapshot(self) -> Dict[str, Any]:
        snap = self._sampler.snapshot()
        return snap or {}

    # Context manager
    def __enter__(self) -> "Monitor":
        return self.start()

    def __exit__(self, exc_type, exc, tb):
        self.stop()

    # Syntactic sugar
    def running(self) -> "Monitor":
        return self
