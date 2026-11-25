from geneweaver.system_info import (
    get_system_metrics,
    get_gpu_info,
)


def test_system_metrics():
    metrics = get_system_metrics()

    assert 0 <= metrics["cpu_percent"] <= 100
    assert 0 <= metrics["memory_percent"] <= 100
    assert metrics["memory_total_gb"] > 0


def test_gpu_detection():
    devices = get_gpu_info()

    assert isinstance(devices, list)
    assert len(devices) > 0
    assert all(isinstance(device, str) for device in devices)