
import platform
import subprocess

import psutil


def get_system_metrics():
    """Return live CPU and memory metrics."""

    memory = psutil.virtual_memory()

    return {
        "cpu_percent": psutil.cpu_percent(interval=None),
        "memory_percent": memory.percent,
        "memory_used_gb": memory.used / (1024 ** 3),
        "memory_total_gb": memory.total / (1024 ** 3),
        "processor": platform.processor(),
        "platform": platform.system(),
    }


def get_gpu_info():
    """Detect installed display adapters on Windows."""

    if platform.system() != "Windows":
        return ["GPU detection currently configured for Windows."]

    command = (
        "Get-CimInstance Win32_VideoController | "
        "Select-Object -ExpandProperty Name"
    )

    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", command],
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        )

        devices = [
            line.strip()
            for line in result.stdout.splitlines()
            if line.strip()
        ]

        return devices or ["No display adapter detected."]

    except (subprocess.SubprocessError, OSError):
        return ["GPU information unavailable."]
