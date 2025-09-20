from pathlib import Path
from codemonitor.sinks.csv_sink import CsvSink

def test_csv_sink(tmp_path: Path):
    sink = CsvSink(tmp_path, max_gpus=2)
    rec = {
        "schema":"codemonitor/1.0",
        "ts_ms":0, "host":"h", "pid":1, "proc_name":"p", "mark":"m",
        "cpu":{"total_pct":1.0,"proc_pct":0.5},
        "ram":{"pct":10,"used_mb":100,"avail_mb":200,"proc_rss_mb":10,"proc_vms_mb":20},
        "gpus":[{"index":0,"name":"X","uuid":"U","util_pct":11,"mem_used_mb":1,"mem_total_mb":2,"power_w":0,"temp_c":0}],
    }
    sink.write(rec)
    sink.close()
    assert (tmp_path / "codemonitor.csv").exists()
