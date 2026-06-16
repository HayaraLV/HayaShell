import os
import platform
import subprocess

# --- Переменные и стилистика ---
SQUARE = "\u2588"

# Фирменные цвета Python (цвета из вашего prompt)
BLUE = "\033[34m"
YELLOW = "\033[33m"  # Заменили яркий 93m на классический 33m для соответствия prompt
RED = "\033[31m"
GREEN = "\033[32m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
RESET = "\033[0m"

CORE_NAME = "py_OS_MK"
VERSION = "v-1.4.1"

# Переменная пользователя (подхватывается из системы, если не задана в Shell)
try:
    current_user = globals().get('CURRENT_USER', os.getlogin())
except Exception:
    current_user = "user"

# --- Кроссплатформенное получение CPU ---
def get_cpu_name():
    try:
        sys_name = platform.system()
        if sys_name == "Windows":
            cmd = "wmic cpu get name"
            name = subprocess.check_output(cmd, shell=True).decode('utf-8')
            return name.replace("Name", "").strip()
        elif sys_name == "Darwin":  # macOS
            cmd = "sysctl -n machdep.cpu.brand_string"
            return subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
        elif sys_name == "Linux":
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "model name" in line:
                        return line.split(":")[1].strip()
        return platform.processor() or "Generic CPU"
    except Exception:
        return "Python Thread CPU"

# --- Кроссплатформенное получение RAM (Чистый Python) ---
def get_ram_info():
    """Возвращает кортеж (использовано_ГБ, всего_ГБ)"""
    sys_name = platform.system()
    total_gb = 4.0  # Дефолтные заглушки на случай полной блокировки прав
    used_gb = 0.5
    
    try:
        if sys_name == "Windows":
            # Используем встроенный wmic для ОЗУ
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
            
        elif sys_name == "Darwin":  # macOS
            cmd_total = "sysctl -n hw.memsize"
            total_bytes = int(subprocess.check_output(cmd_total, shell=True).decode().strip())
            total_gb = total_bytes / (1024 ** 3)
            # Приблизительный расчет для macOS без сторонних либ
            used_gb = total_gb * 0.4 
    except Exception:
        pass
    return f"{used_gb:.1f} GB", f"{total_gb:.1f} GB"
# --- Сбор информации ---
os_name = platform.system()
os_release = platform.release()
py_version = platform.python_version()
node_name = platform.node()    
cpu_name = get_cpu_name()
if len(cpu_name) > 25:
    cpu_name = cpu_name[:22] + "..."
used_ram, total_ram = get_ram_info()
# --- Отрисовка ---
logo = [
    f"          {BLUE}.?77777777777777$.{RESET}            ",
    f"          {BLUE}777..777777777777$+{RESET}           ",
    f"         {BLUE}.77    7777777777$$${RESET}           ",
    f"         {BLUE}.777 .7777777777$$$${RESET}           ",
    f"         {BLUE}.7777777777777$$$$$${RESET}           ",
    f"         {BLUE}..........:77$$$$$$${RESET}           ",
    f"  {BLUE}.77777777777777777$$$$$$$$$.{RESET}{YELLOW}=======.{RESET}  ",
    f" {BLUE}777777777777777777$$$$$$$$$$.{RESET}{YELLOW}========{RESET}  ",
    f"{BLUE}7777777777777777$$$$$$$$$$$$$.{RESET}{YELLOW}========={RESET} ",
    f"{BLUE}77777777777777$$$$$$$$$$$$$$$.{RESET}{YELLOW}========={RESET} ",
    f"{BLUE}777777777777$$$$$$$$$$$$$$$$ {RESET}{YELLOW}:========+.{RESET}",
    f"{BLUE}77777777777$$$$$$$$$$$$$$+..{RESET}{YELLOW}=========++~{RESET}",
    f"{BLUE}777777777$$..~{RESET}{YELLOW}=====================+++++{RESET}",
    f"{BLUE}77777777${RESET}{YELLOW}~.~~~~=~=================+++++.{RESET}",
    f"{BLUE}777777$$$.{RESET}{YELLOW}~~~===================+++++++.{RESET}",
    f"{BLUE}77777$$$$.{RESET}{YELLOW}~~==================++++++++:{RESET} ",
    f" {BLUE}7$$$$$$$.{RESET}{YELLOW}==================++++++++++.{RESET} ",
    f" {BLUE}.,$$$$$$.{RESET}{YELLOW}================++++++++++~.{RESET}  ",
    f"         {YELLOW}.=========~.........{RESET}           ",
    f"         {YELLOW}.=============++++++{RESET}           ",
    f"         {YELLOW}.===========+++..+++{RESET}           ",
    f"         {YELLOW}.==========+++.  .++{RESET}           ",
    f"          {YELLOW},=======++++++,,++,{RESET}           ",
    f"          {YELLOW}..=====+++++++++=.{RESET}            "
]
info = [
    f"{YELLOW}{current_user}{RESET}{BLUE}@{node_name}{RESET}",
    "---------------------------------------",
    f"{YELLOW}OS{RESET}       : {CORE_NAME} {VERSION} ({os_name} {os_release})",
    f"{YELLOW}Host{RESET}     : Python Virtual Machine",
    f"{YELLOW}Shell{RESET}    : Python Terminal Core",
    f"{YELLOW}Language{RESET} : Python {py_version}",
    f"{YELLOW}CPU{RESET}      : {cpu_name}",
    f"{YELLOW}RAM{RESET}      : {used_ram} / {total_ram}",
    f"{YELLOW}Status{RESET}   : Operational",
    f"{YELLOW}Creator{RESET}  : VadimLA",
    "",
    f"{RED}{SQUARE}{SQUARE}{RESET}{GREEN}{SQUARE}{SQUARE}{RESET}{YELLOW}{SQUARE}{SQUARE}{RESET}{BLUE}{SQUARE}{SQUARE}{RESET}{MAGENTA}{SQUARE}{SQUARE}{RESET}{CYAN}{SQUARE}{SQUARE}{RESET}",
    "",
    f"{BLUE}Welcome to your {YELLOW}custom workspace!{RESET}"
]  
print()
for i in range(max(len(logo), len(info))):
    logo_line = logo[i] if i < len(logo) else " " * 40
    info_line = info[i] if i < len(info) else ""
    print(f" {logo_line}  {info_line}")
print()