from __future__ import annotations
import os
import platform
import shutil
from pathlib import Path
from xmrbot.hardware.catalog import catalog


def cpu_model() -> str:
    if Path("/proc/cpuinfo").exists():
        for line in Path("/proc/cpuinfo").read_text(errors="ignore").splitlines():
            if line.lower().startswith("model name"):
                return line.split(":", 1)[1].strip()
    return platform.processor() or "unknown"


def inspect_machine() -> dict:
    model = cpu_model()
    matches = catalog.search(model.replace("Processor", "").strip())
    if not matches:
        # try token match for common model numbers
        tokens = [t for t in model.replace("-", " ").split() if any(c.isdigit() for c in t)]
        for token in tokens:
            found = catalog.search(token)
            if found:
                matches = found
                break
    mem_total = None
    meminfo = Path("/proc/meminfo")
    if meminfo.exists():
        for line in meminfo.read_text().splitlines():
            if line.startswith("MemTotal:"):
                mem_total = int(line.split()[1]) * 1024
                break
    return {
        "cpu_model": model,
        "logical_cpus": os.cpu_count() or 1,
        "ram_bytes": mem_total,
        "os": platform.system(),
        "kernel": platform.release(),
        "xmrig_installed": shutil.which("xmrig") is not None,
        "monerod_installed": shutil.which("monerod") is not None,
        "p2pool_installed": shutil.which("p2pool") is not None,
        "tor_installed": shutil.which("tor") is not None,
        "catalog_match": matches[0].model_dump() if matches else None,
    }


def benchmark_estimate() -> dict:
    machine = inspect_machine()
    match = machine["catalog_match"]
    if match:
        return {
            "mode": "catalog-estimate",
            "hashrate_hs": match["benchmark_hashrate_hs"],
            "watts": match.get("benchmark_watts") or match["tdp_w"],
            "cpu": match["model"],
            "warning": "Estimate only. Run a real XMRig benchmark before purchasing hardware or committing capital.",
        }
    return {
        "mode": "unavailable",
        "hashrate_hs": None,
        "cpu": machine["cpu_model"],
        "warning": "CPU is not in the bundled benchmark catalog. Install XMRig and add a measured benchmark adapter.",
    }
