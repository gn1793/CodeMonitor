import csv
from pathlib import Path
from typing import Dict, List, Optional

from ..schema import flatten_record

class CsvSink:
    def __init__(self, out_dir: Path, max_gpus: int = 4):
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.file = open(self.out_dir / "codemonitor.csv", "w", newline="", encoding="utf-8")
        self.writer = None
        self.header: Optional[List[str]] = None
        self.max_gpus = max_gpus

    def write(self, record: Dict) -> None:
        row = flatten_record(record, max_gpus=self.max_gpus)
        if self.writer is None:
            self.header = list(row.keys())
            self.writer = csv.DictWriter(self.file, fieldnames=self.header)
            self.writer.writeheader()
        self.writer.writerow(row)
        self.file.flush()

    def close(self):
        try:
            self.file.close()
        except Exception:
            pass
