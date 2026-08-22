import time
import os
import shutil
import requests
import sys
import platform
import subprocess
from datetime import datetime
from pathlib import Path
if platform.system() != "Windows":
    import resource
    import ctypes
else:
    import msvcrt
ROOT_NAME = "root"
SQUARE = "\u2588"
RED = "\033[31m"
GREEN = "\033[32m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
BLACK = "\033[30m"
BLUE = "\033[34m"
YELLOW = "\033[93m"
RESET = "\033[0m"
CORE_NAME = "py_OS_MK" #py - python, OS - operational system, MK - micro kernel
VERSION = "1.5.0"
TERMINAL_HISTORY = []
WARN = f"{RED}WARNING: {RESET}"
ERR = f"{RED}ERROR: {RESET}"
def get_ram_info():
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
            cmd_total = "sysctl -n hw.memsize"
            total_bytes = int(subprocess.check_output(cmd_total, shell=True).decode().strip())
            total_gb = total_bytes / (1024 ** 3)
            used_gb = total_gb * 0.4 
    except Exception:
        pass
    return f"{used_gb:.1f} GB", f"{total_gb:.1f} GB"
def print_tree(directory: Path, prefix: str = ""):
    items = sorted(list(directory.iterdir()), key=lambda p: (not p.is_dir(), p.name.lower()))    
    for index, item in enumerate(items):
        is_last = (index == len(items) - 1)
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{item.name}")
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
        elif current_os == "Darwin":  # macOS
            subprocess.Popen(["open", filepath])
        else:  # Linux
            subprocess.Popen(["xdg-open", filepath])
        return True
    except Exception as e:
        print(f"{RED}Error launching file: {RESET} {e}")
        return False
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
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
def check_site(url):
  if not url.startswith(("http://", "https://")):
    url = f"https://{url}"
  try:
    response = requests.head(url, timeout=5)
    if response.status_code == 200:
      print(f"Сайт {url} активен и доступен (Код: {response.status_code})")
    else:
      print(
          f"Сайт {url} вернул ошибку или перенаправление (Код:"
          f" {response.status_code})"
      )
  except requests.ConnectionError:
    print(f"Сайт {url} недоступен (Ошибка подключения/Не существует)")
  except requests.Timeout:
    print(f"Сайт {url} не ответил вовремя (Тайм-аут)")
os_name = platform.system()
os_release = platform.release()
py_version = platform.python_version()
node_name = platform.node()    
cpu_name = get_cpu_name()
used_ram, total_ram = get_ram_info()
commands = {
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
    f"{YELLOW}    curl{RESET}"    : f"Download files from the internet via URL {BLUE}(Usage: curl [url] [output_name]){RESET}",
    f"{YELLOW}    ping{RESET}"    : f"Check URL status {BLUE}(Usage: ping [url]){RESET}",
}
info = [
    f"{YELLOW}root{RESET}{BLUE}@{node_name}{RESET}",
    "---------------------------------------",
    f"{YELLOW}OS{RESET}       : {os_name} {os_release}",
    f"{YELLOW}PY-shell{RESET} : {VERSION}",
    f"{YELLOW}Python{RESET}   : {py_version}",
    f"{YELLOW}CPU{RESET}      : {cpu_name}",
    f"{YELLOW}RAM{RESET}      : {used_ram} / {total_ram}",
    f"{YELLOW}Creator{RESET}  : https://github.com/HayaraLV",
    "",
    f"{RED}{SQUARE}{SQUARE}{RESET}{GREEN}{SQUARE}{SQUARE}{RESET}{YELLOW}{SQUARE}{SQUARE}{RESET}{BLUE}{SQUARE}{SQUARE}{RESET}{MAGENTA}{SQUARE}{SQUARE}{RESET}{CYAN}{SQUARE}{SQUARE}{RESET}",
    "",
    f"{BLUE}Welcome to your {YELLOW}workspace!{RESET}"
]   
slowprint(f"Type '{BLUE}help{RESET}' to see a list of available commands.\n")
while True:
    current_dir = os.path.basename(os.getcwd())
    if not current_dir:
        current_dir = "/"
    user_input = input(f"{YELLOW}{ROOT_NAME}{BLUE}@py-shell:{RESET}[{current_dir}]{BLUE}:~${RESET} ").strip()
    if user_input and not user_input.startswith("history") and user_input != "exit":
        if not user_input:
            continue
        TERMINAL_HISTORY.append(user_input)
    if user_input == "help":
        print("\nAvailable commands:")
        for cmd, desc in commands.items():
            print(f"  {cmd:<20} - {desc}")
        print()
    elif user_input.startswith("tree"):
        parts = user_input.split(maxsplit=1)
        target_path = Path(parts[1]) if len(parts) > 1 else Path(".")
    
        if target_path.exists() and target_path.is_dir():
            print(target_path.name)  # Выводим корень дерева
            print_tree(target_path)
        else:
            print("Error: The specified path does not exist or is not a folder.")
    elif user_input.startswith("note"):
        note = user_input[5:].strip()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        core_dir = os.path.dirname(script_dir)
        notes_filename = os.path.join(core_dir, "user", "notes.txt")
        if not note:
            pass
        elif note == "-c":
            note_delete = input(f"Clear {RED}all{RESET} notes (Y/n)")
            if note_delete == "Y":
                with open(notes_filename, 'w', encoding='utf-8') as f:
                    pass
                print("Notes cleared.")
            else:
                print("Canceled.")
                pass
        elif note.startswith("-t"):
            note = user_input[7:].strip()        
            with open(notes_filename, 'a', encoding='utf-8') as f:
                f.write(datetime.now().strftime("%Y.%m.%d | %H:%M:%S") + "\n")
                f.write(note + "\n\n")
            print(f"{GREEN}Writed{RESET} -> {notes_filename}")
        elif note == "-r":
            with open(notes_filename, 'r', encoding='utf-8') as f:
                content = f.read()
                if not content:
                    print(f"Notes is empty.")
                else:
                    print(f"\n==========Notes==========")
                    print(content)
                    print("=========================\n")
        elif note == "-h":
            print(f"{BLUE}Arguments:{RESET}")
            print(f"    -c -> {YELLOW}Clear all notes.{RESET}")
            print(f"    -r -> {YELLOW}Read all notes.{RESET}")
            print(f"    -t -> {YELLOW}Create note with date and time.{RESET}")
            print(f"    -h -> {YELLOW}Show this owerview.{RESET}")
        elif note != "-c" and note != "-t" and note != "-h" and note != "-r":      
            with open(notes_filename, 'a', encoding='utf-8') as f:
                f.write(note + "\n\n")
            print(f"{GREEN}Writed{RESET} -> {notes_filename}")
    elif user_input.startswith("history"):
        import os
        args = user_input.split()        
        if len(args) > 1 and args[1] == "-c":
            TERMINAL_HISTORY.clear()
        elif len(args) > 1 and args[1] == "-h":
            print("Arguments:")
            print("    -h -> Show this owerview.")
            print("    -c -> Clear command history.")
        elif user_input == "history":
            if not TERMINAL_HISTORY:
                print("История пуста.")
            for index, cmd in enumerate(TERMINAL_HISTORY, 1):
                print(f" {index}  {cmd}")                
        else:
            print(f"Unknown argument. Use 'history' or 'history -c'")
    elif user_input.startswith("run "):
        raw_path = user_input[4:].strip()
        filename = raw_path.strip('"').strip("'")
        if os.path.exists(filename):
            ext = os.path.splitext(filename)[1].lower()
            sys_name = platform.system()
            is_ios = False                                        
            if sys_name not in ["Windows", "Linux", "Darwin"]:
                is_ios = True
            elif "com.blinksh" in os.environ.get("HOME", "") or "documents" in os.environ.get("HOME", "").lower():
                is_ios = True
            if is_ios and ext != ".py":
                print(f"{RED}Access Denied: iOS environment blocks execution of '{ext}' files.{RESET}")
                continue
            elif sys_name == "Windows" and ext not in [".py", ".exe", ".bat", ".cmd", ".lnk"]:
                print(f"{RED}Error: Windows core cannot run '{ext}' files via this command.{RESET}")
                print(f"{YELLOW}Allowed formats: .py, .exe, .bat, .cmd, .lnk{RESET}")
                continue
            elif sys_name in ["Linux", "Darwin"] and ext not in [".py", ".sh", ""]:
                print(f"{RED}Error: Unix environment cannot run '{ext}' files.{RESET}")
                continue
            print(f"\033[34m[Launch {filename}...]\033[0m")         
            try:
                if ext == ".py":                                    
                    with open(filename, "r", encoding="utf-8") as f:
                        ile_code = f.read()
                    sandbox_globals = globals().copy()             
                    sandbox_globals["current_user"] = "root"
                    sandbox_globals["VERSION"] = VERSION
                    sandbox_locals = {}
                    exec(file_code, sandbox_globals, sandbox_locals)
                elif sys_name == "Windows" and ext == ".lnk":                                      
                    subprocess.run(f'start "" "{filename}"', shell=True, check=True)                
                else:                                                                              
                    if sys_name == "Windows":
                        subprocess.run(f'"{filename}"', shell=True, check=True)
                    else:
                        if not os.access(filename, os.X_OK):
                            os.chmod(filename, 0o755)
                        subprocess.run([filename], check=True)
            except Exception as e:
                print(f"{RED}Error while executing the script:{RESET} {e}")
            print(f"{YELLOW}[Kernel] {RESET}Initializing.{RESET}")                                 
            scale_width = 30                                                                       
            for i in range(scale_width + 1):
                percent = int((i / scale_width) * 100)
                bar = SQUARE * i + " " * (scale_width - i)            
                sys.stdout.write(f"\r{RESET}[{bar}]{RESET} {percent}% ")
                sys.stdout.flush()
                time.sleep(0.015)                                                       
            print(f"\n{BLUE}[Success]{RESET} {filename}\n")
        else:
            print(f"{RED}File {RESET}'{filename}'{RED} not found.{RESET}")
    elif user_input == "clear":
        clear_arg = user_input[5:].strip()
        if not clear_arg:
            os.system('cls' if os.name == 'nt' else 'clear')
    elif user_input.startswith("date"):
        date_arg = user_input[4:].strip()
        if not date_arg:
            now = datetime.now()
            formatted_date = now.strftime("%Y.%m.%d | %H:%M:%S")
            print(formatted_date)
        else:
            if date_arg.startswith("-h"):
                print(f"{BLUE}Arguments [help]:{RESET}")
                print(f"{YELLOW}    -h {RESET}->{BLUE} Show this owerview{RESET}")
                print(f"{YELLOW}    -f {RESET}->{BLUE} Write the current date to a file{RESET}")
            if date_arg.startswith("-f"):
                formatted_date = datetime.now().strftime("%Y.%m.%d | %H:%M:%S")
                filename = "datetime.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(formatted_date)
                    print(f"Written to -> {filename} | directory -> {current_dir}")
    elif user_input == "ls":
        files = os.listdir('.')
        if not files:
            slowprint(f"{RED}Directory is empty.{RESET}")
        else:
            slowprint("\nContents of current directory:")
            for item in files:
                if os.path.isdir(item):
                    slowprint(f"  [DIR]  {item}")
                else:
                    slowprint(f"  [FILE] {item}")
            print()
    elif user_input == "mkdir":
        folder_name = input("Enter new directory name: ").strip()        
        if not folder_name:
            slowprint(f"{RED}Error: Directory name cannot be empty.{RESET}")
        else:
            try:
                os.makedirs(folder_name)
                slowprint(f"{GREEN}Directory{RESET} '{folder_name}' {GREEN}successfully created.{RESET}")
            except FileExistsError:
                slowprint(f"{YELLOW}Error: Directory{RESET} '{folder_name}' {YELLOW}already exists.{RESET}")
            except Exception as e:
                slowprint(f"{RED}Error: Could not create directory. {RESET}Reason: {e}")
    elif user_input.startswith("cd"):
        target_dir = user_input[2:].strip()    
        if not target_dir:
            print(f"{BLUE}Usage: cd [directory_name]{RESET}")
        else:
            try:
                os.chdir(target_dir)
            except Exception as e:
                print(f"{RED}Error:{RESET} {e}")
    elif user_input.startswith("touch "):
        filename = user_input[6:].strip()
        if not filename:
            print("Error: Please specify a filename. Usage: touch [filename.txt]")
        else:
            try:
                with open(filename, 'a', encoding='utf-8') as f:
                    pass
                print(f"Created file: {filename}")
            except Exception as e:
                print(f"Error: Could not create file. Reason: {e}")
    elif user_input.startswith("echo "):
        raw_content = user_input[5:].strip()        
        if ">" in raw_content:
            text_to_save, filename = raw_content.split(">", 1)
            text_to_save = text_to_save.strip()
            filename = filename.strip()
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(text_to_save)
                print(f"Written to {filename}")
            except Exception as e:
                print(f"Error writing to file: {e}")
        else:
            print(raw_content)
    elif user_input.startswith("edit "):
        filename = user_input[5:].strip()
        if not filename:
            print(f"{RED}Error: Please specify a file name. Usage: edit [file_name]{RESET}")
            continue
        print(f"\033[34m=== OS.PY Text Editor ===\033[0m")
        print(f"Editing: {YELLOW}{filename}{RESET}")
        print("Type your text. To SAVE and EXIT, type \033[32m:q\033[0m on a new line.\n")
        lines = []
        if os.path.exists(filename) and os.path.isfile(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                for line in lines:
                    print(line, end="")
            except Exception as e:
                print(f"{RED}Error reading file:{RESET} {e}")
        while True:
            try:
                line = input()
                if line.strip() == ":q":
                    break
                lines.append(line + "\n")
            except (KeyboardInterrupt, EOFError):
                print("\nUse :q on a new line to save and exit.")
                break        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.writelines(lines)
            print(f"\n{GREEN}[+] File '{filename}' successfully saved!{RESET}\n")
        except Exception as e:
            print(f"\n{RED}Error saving file:{RESET} {e}\n")
    elif user_input.startswith("cat "):
        filename = user_input[4:].strip()        
        if not filename:
            print("Error: Please specify a filename. Usage: cat [filename.txt]")
        else:
            if not os.path.exists(filename):
                print(f"Error: File '{filename}' does not exist.")
            elif os.path.isdir(filename):
                print(f"Error: '{filename}' is a directory, not a file.")
            else:
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if not content:
                        print(f"[ File '{filename}' is empty ]")
                    else:
                        print(f"\n--- Reading: {filename} ---")
                        # Выводим текст красиво и плавно
                        print(content)
                        print("-------------------------\n")
                        
                except Exception as e:
                    print(f"Error: Could not read file. Reason: {e}")
    elif user_input.startswith("rm "):
        target = user_input[3:].strip()
        if not target:
            print("Error: Please specify a file or directory to remove. Usage: rm [name]")
        elif not os.path.exists(target):
            print(f"Error: '{target}' does not exist.")
        else:
            try:
                if os.path.isdir(target):
                    if not os.listdir(target):
                        os.rmdir(target)
                        print(f"Directory '{target}' successfully removed.")
                    else:
                        confirm = input(f"Directory '{target}' is not empty. Delete anyway? (Y/n): ").strip().lower()
                        if confirm == 'Y':
                            shutil.rmtree(target)
                            print(f"Directory '{target}' and all its contents removed.")
                else:
                    confirm = input(f"Delete {target} (Y/n): ")
                    if confirm == 'Y':
                        os.remove(target)
                        print(f"File '{target}' successfully removed.")
            except Exception as e:
                print(f"Error: Could not remove '{target}'. Reason: {e}")
    elif user_input.startswith("cp "):
        parts = user_input[3:].strip().split(" ")
        if len(parts) >= 2:
            src, dst = parts[0], parts[1]
            try:
                import shutil
                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                else:
                    shutil.copy(src, dst)
                print(f"{GREEN}Successfully copied to {dst}{RESET}")
            except Exception as e:
                print(f"{RED}Error:{RESET} {e}")
        else:
            print(f"{RED}Usage: cp [source] [destination]{RESET}")
    elif user_input.startswith("mv "):
        parts = user_input[3:].strip().split(" ")
        if len(parts) >= 2:
            src, dst = parts[0], parts[1]
            try:
                os.rename(src, dst)
                print(f"{GREEN}Successfully moved/renamed to {dst}{RESET}")
            except Exception as e:
                print(f"{RED}Error:{RESET} {e}")
        else:
            print(f"{RED}Usage: mv [source] [destination]{RESET}")
    elif user_input.startswith("grep "):
        keyword = user_input[5:].strip()
        if keyword:
            found = False
            for item in os.listdir('.'):
                if os.path.isfile(item) and item.endswith('.py') or item.endswith('.txt'):
                    try:
                        with open(item, 'r', encoding='utf-8') as f:
                            for idx, line in enumerate(f, 1):
                                if keyword in line:
                                    print(f"{BLUE}{item}:{idx}{RESET} -> {line.strip()}")
                                    found = True
                    except:
                        pass
            if not found:
                print(f"{YELLOW}No matches found for '{keyword}'{RESET}")
        else:
            print(f"{RED}Usage: grep [text_to_find]{RESET}")
    elif user_input.startswith("curl "):
        cmd_args = user_input[5:].strip()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        core_dir = os.path.dirname(script_dir)
        filename = os.path.join(core_dir, "utilities", "curl.py")
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    file_code = f.read()
                context = globals().copy()
                context["context_args"] = cmd_args
                exec(file_code, context)
            except Exception as e:
                print(f"{RED}Error in curl:{RESET} {e}")
        else:
            print(f"{RED}FNF: {filename} not found{RESET}")
    elif user_input.startswith("ping "):
        cmd_args = user_input[5:].strip()
        check_site(cmd_args)
    elif user_input.startswith("sys "):
        sys_arg = user_input[4:].strip()
        if not sys_arg:
            print("Try sys -i || sys -h")
        elif sys_arg == "-i":
            logo_dir = os.path.dirname(os.path.abspath(__file__))
            core_dir = os.path.dirname(logo_dir)
            logo_filename = os.path.join(core_dir, "configs", "logo.cfg")
            with open(logo_filename, 'r', encoding='utf-8') as file:
                logo_code = file.read()
            exec(logo_code)
            print()
            for i in range(max(len(logo), len(info))):
                logo_line = logo[i] if i < len(logo) else " " * 40
                info_line = info[i] if i < len(info) else ""
                print(f" {logo_line}  {info_line}")
            print()
        elif sys_arg == "-h":
            print(f"{BLUE}Arguments:{RESET}")
            print(f"    -i -> {YELLOW}Show system info.{RESET}")
            print(f"    -h -> {YELLOW}Show this owerview.{RESET}")
    elif user_input == "exit":
        sys.exit()
    elif not user_input:
        continue
    else:
        clean_input = user_input.strip('"\'')
        if os.path.exists(clean_input) and os.path.isfile(clean_input):
            print(f"Launching '{clean_input}' via system core...")
            launch_file(clean_input)
        else:
            print("Unknown command or file. Type 'help' to see available commands.")
