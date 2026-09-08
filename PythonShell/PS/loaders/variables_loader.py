import subprocess
import platform
from pathlib import Path
from loaders.variables_loader import *
from loaders.functions_loader import *
from loaders.color_loader import *
def get_ram_info():
    sys_name = platform.system()
    total_gb = "UNK"
    used_gb = "UNK"
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
            cmd_total = "sysctl -n hw.memsize"
            total_bytes = int(subprocess.check_output(cmd_total, shell=True).decode().strip())
            total_gb = total_bytes / (1024 ** 3)
            used_gb = total_gb * 0.4 
    except Exception:
        pass
    return f"{used_gb:.1f} GB", f"{total_gb:.1f} GB"
def get_cpu_name():
    try:
        sys_name = platform.system()
        if sys_name == "Windows":
            cmd = "wmic cpu get name"
            name = subprocess.check_output(cmd, shell=True).decode('utf-8')
            return name.replace("Name", "").strip()
        elif sys_name == "Darwin":
            cmd = "sysctl -n machdep.cpu.brand_string"
            return subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
        elif sys_name == "Linux":
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "model name" in line:
                        return line.split(":")[1].strip()
        return platform.processor() or "Generic Processor"
    except Exception:
        return "Intel/AMD Processor"
os_name = platform.system()
os_release = platform.release()
py_version = platform.python_version()
node_name = platform.node()    
cpu_name = get_cpu_name()
used_ram, total_ram = get_ram_info()
DEFAULT_VARIABLES = {
    "VERSION" : "PY-shell",
    "TERMINAL_HISTORY" : [],
    "WARN" : "\033[31mWARNING -> \033[0m",
    "ERR" : "\033[31mERROR -> \033[0m",
}
def _load_variables():
    variables = DEFAULT_VARIABLES.copy()
    current_file = Path(__file__).resolve()  
    loaders_dir = current_file.parent        
    pyos_dir = loaders_dir.parent           
    project_root = pyos_dir.parent          
    variables_file = project_root / "PS" / "configs" / "variables.cfg"
    try:
        with open(variables_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                value = value.replace('\\033', '\033').replace('\\u2588', '\u2588')
                if key in variables:
                    variables[key] = value
    except FileNotFoundError:
        print(f"{WARN}: file {variables_file} not found, using standart variables.")
    except Exception as e:
        print(f"{WARN}: error read variables.cfg ({e}). standart variables.")
    return variables
_variables = _load_variables()
WARN = f"\033[31mWARNING -> \033[0m"
ERR  = f"\033[31mERROR -> \033[0m"
VERSION = _variables["VERSION"]
TERMINAL_HISTORY = _variables["TERMINAL_HISTORY"]