from codemonitor.probes import cpu_ram

def test_probe_cpu_ram():
    d = cpu_ram.probe()
    assert "cpu" in d and "ram" in d
