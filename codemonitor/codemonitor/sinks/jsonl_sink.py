import json
from pathlib import Path
from typing import Dict

class JsonlSink:
    def __init__(self, out_dir: Path):
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.file = open(self.out_dir / "codemonitor.jsonl", "a", encoding="utf-8")

    def write(self, record: Dict) -> None:
        self.file.write(json.dumps(record, ensure_ascii=False) + "\n")
        self.file.flush()

    def close(self):
        try:
            self.file.close()
        except Exception:
            pass
