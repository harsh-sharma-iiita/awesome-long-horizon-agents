"""Environment diagnostic script for G4 research project.

Determines OS, Python version, CPU, RAM, GPU/CUDA, disk storage,
environment variables, and relevant installed packages.
"""

import os
import platform
import sys
import shutil

try:
    import psutil
except ImportError:
    psutil = None

try:
    import torch
except ImportError:
    torch = None

def get_cpu_info():
    info = {
        "processor": platform.processor(),
        "machine": platform.machine(),
        "logical_cores": os.cpu_count(),
    }
    if psutil:
        info["physical_cores"] = psutil.cpu_count(logical=False)
        cpu_freq = psutil.cpu_freq()
        info["freq_mhz"] = cpu_freq.current if cpu_freq else "Unknown"
    return info

def get_ram_info():
    if psutil:
        mem = psutil.virtual_memory()
        return {
            "total_gb": round(mem.total / (1024**3), 2),
            "available_gb": round(mem.available / (1024**3), 2),
            "used_gb": round(mem.used / (1024**3), 2),
            "percent_used": mem.percent
        }
    return {"status": "psutil not available"}

def get_disk_info(path="."):
    total, used, free = shutil.disk_usage(path)
    return {
        "drive": os.path.abspath(path)[:3],
        "total_gb": round(total / (1024**3), 2),
        "used_gb": round(used / (1024**3), 2),
        "free_gb": round(free / (1024**3), 2),
    }

def get_gpu_info():
    if torch is None:
        return {"torch_installed": False, "cuda_available": False}
    cuda_avail = torch.cuda.is_available()
    info = {
        "torch_version": torch.__version__,
        "cuda_available": cuda_avail,
        "device_count": torch.cuda.device_count() if cuda_avail else 0
    }
    if cuda_avail:
        info["device_name"] = torch.cuda.get_device_name(0)
    return info

def get_api_env_vars():
    keys = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY"]
    status = {}
    for k in keys:
        val = os.environ.get(k)
        status[k] = "SET (masked)" if val else "NOT SET"
    return status

def main():
    print("=" * 60)
    print("G4 RESEARCH PROJECT — SYSTEM ENVIRONMENT DIAGNOSTIC")
    print("=" * 60)
    
    print("\n[OPERATING SYSTEM]")
    print(f"OS: {platform.system()} {platform.release()} (Version: {platform.version()})")
    print(f"Platform: {platform.platform()}")
    
    print("\n[PYTHON ENVIRONMENT]")
    print(f"Python Executable: {sys.executable}")
    print(f"Python Version: {platform.python_version()} ({platform.python_compiler()})")
    print(f"In Virtual Env: {sys.prefix != sys.base_prefix}")
    print(f"Prefix: {sys.prefix}")
    print(f"Base Prefix: {sys.base_prefix}")
    
    print("\n[CPU & PROCESSOR]")
    cpu = get_cpu_info()
    for k, v in cpu.items():
        print(f"{k}: {v}")
        
    print("\n[MEMORY (RAM)]")
    ram = get_ram_info()
    for k, v in ram.items():
        print(f"{k}: {v}")
        
    print("\n[STORAGE DISK]")
    disk = get_disk_info(".")
    for k, v in disk.items():
        print(f"{k}: {v}")
        
    print("\n[ACCELERATOR / GPU]")
    gpu = get_gpu_info()
    for k, v in gpu.items():
        print(f"{k}: {v}")
        
    print("\n[API KEYS / EXTERNAL CREDENTIALS]")
    api = get_api_env_vars()
    for k, v in api.items():
        print(f"{k}: {v}")
        
    print("\n[CORE SCIENTIFIC LIBRARIES]")
    packages = ["numpy", "scipy", "pandas", "networkx", "psutil"]
    for pkg in packages:
        try:
            mod = __import__(pkg)
            ver = getattr(mod, "__version__", "installed")
            print(f"{pkg}: {ver}")
        except ImportError:
            print(f"{pkg}: NOT INSTALLED")
            
    print("=" * 60)

if __name__ == "__main__":
    main()
