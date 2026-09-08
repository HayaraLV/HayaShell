import time
import os
import requests
import sys
import platform
import subprocess
import importlib.util
from datetime import datetime
from pathlib import Path
if platform.system() != "Windows":
    import resource
    import ctypes
else:
    import msvcrt
from loaders.color_loader import *
from loaders.variables_loader import *
from loaders.functions_loader import *
def _load_module(module_name, filepath):
    try:
        filepath = Path(filepath)
        if not filepath.exists():
            return None
        
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        if spec is None or spec.loader is None:
            return None
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"Error to load {module_name}: {e}")
        return None
help_texts = {
    f"{BLUE}System:{RESET}":"",
    f"{YELLOW}    help{RESET}"    : f"Show this overview",
    f"{YELLOW}    date{RESET}"    : f"Show current date | time {BLUE}(Args: -h -f){RESET}",
    f"{YELLOW}    note{RESET}"    : f"Create notes {BLUE}(Args: -h -r -t -c){RESET}",
    f"{YELLOW}    clear{RESET}"   : f"Clear the terminal screen",
    f"{YELLOW}    sys{RESET}"     : f"Show system information (Args: -h -i)",
    f"{YELLOW}    history{RESET}" : f"Show command history {BLUE}(Usage: history (Args: -h -c)){RESET}",
    f"{YELLOW}    exit{RESET}"    : f"Shutdown the system",
    f"{BLUE}Files:{BLUE}":"",
    f"{YELLOW}    ls{RESET}"      : f"List directory contents",
    f"{YELLOW}    tree{RESET}"    : f"Tree of directory contents",
    f"{YELLOW}    cd{RESET}"      : f"Change current directory {BLUE}(Usage: cd [directory_name]){RESET}",
    f"{YELLOW}    mkdir{RESET}"   : f"Create a new directory",
    f"{YELLOW}    touch{RESET}"   : f"Create a new empty file {BLUE}(Usage: touch [file_name]){RESET}",
    f"{YELLOW}    cat{RESET}"     : f"Read and display file contents {BLUE}(Usage: cat [file_name]){RESET}",
    f"{YELLOW}    edit{RESET}"    : f"Open text editor to modify a file {BLUE}(Usage: edit [file_name]){RESET}",
    f"{YELLOW}    echo{RESET}"    : f"Write text to file {BLUE}(Usage: echo [text] > [file_name]){RESET}",
    f"{YELLOW}    cp{RESET}"      : f"Copy a file or directory {BLUE}(Usage: cp [source] [destination]){RESET}",
    f"{YELLOW}    mv{RESET}"      : f"Move or rename a file or directory {BLUE}(Usage: mv [source] [destination]){RESET}",
    f"{YELLOW}    rm{RESET}"      : f"Remove a file or a directory {BLUE}(Usage: rm [file_name]){RESET}",
    f"{YELLOW}    grep{RESET}"    : f"Search for text pattern inside files {BLUE}(Usage: grep [text]){RESET}",
    f"{YELLOW}    run{RESET}"     : f"Execute files and scripts {BLUE}(Usage: run [file_name]){RESET}",
    f"{BLUE}Network:{RESET}":"",
    f"{YELLOW}    wifi{RESET}"    : f"Manage Wi-Fi connections {BLUE}(Usage: wifi (Args: -l -c -d)){RESET}",
    f"{YELLOW}    curl{RESET}"    : f"Download files from the internet via URL {BLUE}(Usage: curl [url] [output_name]){RESET}",
    f"{YELLOW}    ping{RESET}"    : f"Check URL status {BLUE}(Usage: ping [url]){RESET}",
}
def help_command(args):
    print("\nAvailable commands:")
    for cmd, desc in help_texts.items():
        print(f"  {cmd:<20} - {desc}")
    print()
def print_tree(directory: Path, prefix: str = ""):
    items = sorted(list(directory.iterdir()), key=lambda p: (not p.is_dir(), p.name.lower()))
    for index, item in enumerate(items):
        is_last = (index == len(items) - 1)        
        connector = "└── " if is_last else "├── "        
        print(f"{prefix}{connector}{RESET}{item.name}", sep="")
        if item.is_dir():
            next_prefix = prefix + ("    " if is_last else "│   ")
            print_tree(item, next_prefix)
def slowprint(text, speed=0.0001):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()
def ram_used():
    try:
        sys_name = platform.system()
        if sys_name == "Windows":
            cmd = "wmic process where processid=" + str(os.getpid()) + " get WorkingSetSize"
            output = subprocess.check_output(cmd, shell=True).decode().split()
            if len(output) > 1:
                return int(output[1]) / (1024 ** 3)
        elif sys_name in ["Darwin", "Linux"]:
            usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            if sys_name == "Linux":
                return usage / (1024 ** 2)
            return usage / (1024 ** 3)
    except Exception:
        pass
    return 0.04
def ram_total():
    sys_name = platform.system()
    total_gb = 4.0
    used_gb = 0.5
    try:
        if sys_name == "Windows":
            cmd_total = "wmic computersystem get totalphysicalmemory"
            total_bytes = int(subprocess.check_output(cmd_total, shell=True).decode().split()[1])
            total_gb = total_bytes / (1024 ** 3)
            cmd_free = "wmic os get freephysicalmemory"
            free_kb = int(subprocess.check_output(cmd_free, shell=True).decode().split()[1])
            used_gb = total_gb - (free_kb / (1024 ** 2))
        elif sys_name == "Linux":
            with open("/proc/meminfo", "r") as f:
                mem_info = {line.split(":")[0]: int(line.split(":")[1].split()[0]) for line in f}
            total_gb = mem_info["MemTotal"] / (1024 ** 2)
            free_mem = mem_info.get("MemAvailable", mem_info.get("MemFree", 0))
            used_gb = total_gb - (free_mem / (1024 ** 2))
        elif sys_name == "Darwin":
            libc = ctypes.CDLL(None)
            total_mem = ctypes.c_uint64()
            size = ctypes.c_size_t(ctypes.sizeof(total_mem))
            libc.sysctlbyname(b"hw.memsize", ctypes.byref(total_mem), ctypes.byref(size), None, 0)
            total_gb = total_mem.value / (1024 ** 3)
            used_gb = total_gb * 0.40
    except Exception:
        pass
    return f"{used_gb:.2f} GB / {total_gb:.1f} GB"
def ios_vram():
    sys_name = platform.system()
    try:
        if sys_name == "Windows":
            cmd = "wmic path win32_VideoController get AdapterRAM"
            output = subprocess.check_output(cmd, shell=True).decode().split()
            if len(output) > 1:
                return f"{int(output[1]) / (1024 ** 3):.1f} GB"
        elif sys_name == "Darwin":
            libc = ctypes.CDLL(None)
            total_mem = ctypes.c_uint64()
            size = ctypes.c_size_t(ctypes.sizeof(total_mem))
            libc.sysctlbyname(b"hw.memsize", ctypes.byref(total_mem), ctypes.byref(size), None, 0)
            return f"{(total_mem.value / (1024 ** 3)) * 0.65:.1f} GB (Unified)"
    except Exception:
        pass
    return "Shared VRAM"
def launch_file(filepath):
    try:
        current_os = platform.system()
        if current_os == "Windows":
            subprocess.Popen(filepath, shell=True)
        elif current_os == "Darwin":
            subprocess.Popen(["open", filepath])
        else:
            subprocess.Popen(["xdg-open", filepath])
        return True
    except Exception as e:
        print(f"{RED}Error launching file: {RESET} {e}")
        return False
def check_site(url):
  if not url.startswith(("http://", "https://")):
    url = f"https://{url}"
  try:
    response = requests.head(url, timeout=5)
    if response.status_code == 200:
      print(f"site {url} is aviable (status: {response.status_code})")
    else:
      print(
          f"site {url} (Status:"
          f" {response.status_code})")
  except requests.ConnectionError:
    print(f"site {url} unaviable")
  except requests.Timeout:
    print(f"site {url} (Time-out)")
def _load_all_functions():
    functions = {}
    current_dir = Path(__file__).resolve().parent
    pyos_dir = current_dir.parent
    functions_dir = pyos_dir / "functions"
    if not functions_dir.exists():
        return functions
    for filepath in functions_dir.glob("*.py"):
        if filepath.name == "__init__.py":
            continue
        module_name = filepath.stem
        module = _load_module(module_name, filepath)
        if module:
            functions[module_name] = module
            for attr_name in dir(module):
                if not attr_name.startswith('_'):
                    attr = getattr(module, attr_name)
                    if callable(attr):
                        globals()[attr_name] = attr
    return functions
functions = _load_all_functions()