from codemonitor.probes import nvidia

def test_probe_gpu():
    # Should not raise even if NVML missing
    g = nvidia.probe_all()
    assert isinstance(g, list)
