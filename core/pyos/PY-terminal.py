import time
import os
import sys
import platform
import subprocess
from pathlib import Path
if platform.system() != "Windows":# Безопасно импортируем специфичные библиотеки (чтобы скрипт не падал на Windows)
    import resource
    import ctypes
else:
    import msvcrt
from datetime import datetime
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
BOLD = "\033[1m"
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"
CORE_NAME = "py_OS_MK" #py - python, OS - operational system, MK - micro kernel
VERSION = "v-1.4.1"
TERMINAL_HISTORY = []
def print_tree(directory: Path, prefix: str = ""):
    """Рекурсивно выводит дерево файлов и папок."""
    # Получаем список всех элементов и сортируем их (сначала папки, потом файлы)
    items = sorted(list(directory.iterdir()), key=lambda p: (not p.is_dir(), p.name.lower()))
    
    for index, item in enumerate(items):
        # Проверяем, является ли элемент последним в текущей папке
        is_last = (index == len(items) - 1)
        
        # Выбираем правильные символы для ветки
        connector = "└── " if is_last else "├── "
        
        # Выводим имя элемента с нужным отступом
        print(f"{prefix}{connector}{item.name}")
        
        # Если это папка, заходим внутрь (рекурсия)
        if item.is_dir():
            # Настраиваем отступ для подпапок
            next_prefix = prefix + ("    " if is_last else "│   ")
            print_tree(item, next_prefix)
def slowprint(text, speed=0.0001):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()
def ios_ram_used():
    """Кроссплатформенный подсчет оперативной памяти, занятой текущим процессом"""
    try:
        sys_name = platform.system()
        if sys_name == "Windows":
            # Используем встроенный wmic для Windows
            cmd = "wmic process where processid=" + str(os.getpid()) + " get WorkingSetSize"
            output = subprocess.check_output(cmd, shell=True).decode().split()
            if len(output) > 1:
                return int(output[1]) / (1024 ** 3)
        elif sys_name in ["Darwin", "Linux"]:
            # Для Linux/macOS используем resource
            usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            # В Linux ru_maxrss возвращается в Килобайтах, в macOS/iOS в Байтах
            if sys_name == "Linux":
                return usage / (1024 ** 2)
            return usage / (1024 ** 3)
    except Exception:
        pass
    return 0.04 # Заглушка-минимум, если права ограничены
def ios_ram():
    """Кроссплатформенный сбор информации об ОЗУ всей ОС (Использовано / Всего)"""
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
        elif sys_name == "Darwin": # macOS / iOS
            # Динамический вызов ctypes вынесен в try блок
            libc = ctypes.CDLL(None)
            total_mem = ctypes.c_uint64()
            size = ctypes.c_size_t(ctypes.sizeof(total_mem))
            libc.sysctlbyname(b"hw.memsize", ctypes.byref(total_mem), ctypes.byref(size), None, 0)
            total_gb = total_mem.value / (1024 ** 3)
            used_gb = total_gb * 0.40 # Базовая аппроксимация без psutil
    except Exception:
        pass
    return f"{used_gb:.2f} GB / {total_gb:.1f} GB"
def ios_vram():
    """Кроссплатформенный сбор информации о видеопамяти"""
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
slowprint(f"Welcome back, root.")
print("Type 'help' to see a list of available commands.\n")
while True:
    current_dir = os.path.basename(os.getcwd())
    if not current_dir:
        current_dir = "/"
    user_input = input(f"{YELLOW}root{BLUE}@os.py-shell:{RESET}[{current_dir}]{BLUE}:~${RESET} ").strip()
    
    # --- ДОБАВИТЬ СЮДА: Запись каждой команды в файл ---
    if user_input and not user_input.startswith("history") and user_input != "exit":
        if not user_input:
            continue
        TERMINAL_HISTORY.append(user_input)
    # --------------------------------------------------
    if user_input == "help":
        script_dir = os.path.dirname(os.path.abspath(__file__))     
        core_dir = os.path.dirname(script_dir)                      
        filename = os.path.join(core_dir, "commands", "help.py")    
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    file_code = f.read()
                exec(file_code, globals())
            except Exception as e:
                print(f"{RED}Error:{RESET} {e}")
        else:
            print(f"{RED}FNF: {filename} not found{RESET}")
    elif user_input.startswith("tree"):
        parts = user_input.split(maxsplit=1)
        target_path = Path(parts[1]) if len(parts) > 1 else Path(".")
    
        if target_path.exists() and target_path.is_dir():
            print(target_path.name)  # Выводим корень дерева
            print_tree(target_path)
        else:
            print("Ошибка: Указанный путь не существует или не является папкой.")

    elif user_input.startswith("history"):
        import os
        args = user_input.split()        
        if len(args) > 1 and args[1] == "-c":
            # Очистка списка в памяти
            TERMINAL_HISTORY.clear()
                
        elif user_input == "history":
            if not TERMINAL_HISTORY:
                print("История пуста.")
            for index, cmd in enumerate(TERMINAL_HISTORY, 1):
                print(f" {index}  {cmd}")
                            
        else:
            print(f"Неизвестный аргумент. Используйте 'history' или 'history -c'")
    elif user_input.startswith("run "):
        raw_path = user_input[4:].strip()
        # ... ваш существующий код для run ...
                        # Берем всё, что после "run ", убирая лишние пробелы по краям
        filename = raw_path.strip('"').strip("'")                   # Очищаем путь от кавычек, если пользователь ввёл их вручную (например, run "Unreal Engine.lnk")
        if os.path.exists(filename):
            ext = os.path.splitext(filename)[1].lower()
            sys_name = platform.system()
            is_ios = False                                          # 1. ОПРЕДЕЛЯЕМ ПЛАТФОРМУ (iOS / Android / PC)
            if sys_name not in ["Windows", "Linux", "Darwin"]:
                is_ios = True
            elif "com.blinksh" in os.environ.get("HOME", "") or "documents" in os.environ.get("HOME", "").lower():
                is_ios = True
            if is_ios and ext != ".py":                             # ЭТАП 2: ФИЛЬТРЫ СОВМЕСТИМОСТИ СРЕДЫ
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
                    # Оборачиваем в кавычки для защиты от пробелов в путях на Windows
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
        os.system('cls' if os.name == 'nt' else 'clear')
    elif user_input == "date":
        # 1. Получаем путь к папке 'pyos', где лежит сам скрипт
        script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Поднимаемся на уровень вверх в папку 'core'
        core_dir = os.path.dirname(script_dir)
    
    # 3. Строим точный путь к help.py внутри core/commands/
        filename = os.path.join(core_dir, "commands", "date.py")

        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    file_code = f.read()
                exec(file_code, globals())
            except Exception as e:
                print(f"{RED}Error:{RESET} {e}")
        else:
            print(f"{RED}FNF: {filename} not found{RESET}")	     
    elif user_input == "ls":
        # Получаем список всех файлов и папок в текущей директории
        files = os.listdir('.')
        if not files:
            slowprint(f"{RED}Directory is empty.{RESET}")
        else:
            slowprint("\nContents of current directory:")
            for item in files:
                # Проверяем, является ли объект папкой, чтобы добавить красивый маркер
                if os.path.isdir(item):
                    slowprint(f"  [DIR]  {item}")
                else:
                    slowprint(f"  [FILE] {item}")
            print() # Пустая строка для красоты
    elif user_input == "mkdir":
        folder_name = input("Enter new directory name: ").strip()
        
        # Проверяем, что пользователь не ввел пустую строку
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
    # Отрезаем слово "cd" и пробел, оставляем только путь к папке
    # (если ввели просто "cd", останется пустая строка)
        target_dir = user_input[2:].strip()
    
    # Если ввели просто "cd" без параметров, выводим подсказку
        if not target_dir:
            print(f"{BLUE}Usage: cd [directory_name]{RESET}")
        else:
            try:
            # Меняем папку напрямую в главном процессе терминала
                os.chdir(target_dir)
            except Exception as e:
            # Если папки нет или к ней нет доступа, выводим системную ошибку
                print(f"{RED}Error:{RESET} {e}")
    elif user_input.startswith("touch "):
        filename = user_input[6:].strip()
        if not filename:
            print("Error: Please specify a filename. Usage: touch [filename.txt]")
        else:
            try:
                # Открываем в режиме 'a' и сразу закрываем — это создает пустой файл
                with open(filename, 'a', encoding='utf-8') as f:
                    pass
                # В Linux touch работает молча, но для псевдо-ОС можно оставить короткий лог:
                print(f"Created file: {filename}")
            except Exception as e:
                print(f"Error: Could not create file. Reason: {e}")
    elif user_input.startswith("echo "):
        # Отрезаем слово "echo "
        raw_content = user_input[5:].strip()
        
        # Проверяем, есть ли в строке символ ">" для записи в файл
        if ">" in raw_content:
            # Разделяем текст и имя файла
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
            # Если стрелочки ">" нет, просто выводим текст в консоль (как в обычном Linux)
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
        # Если файл уже существует, сначала прочитаем его содержимое
        if os.path.exists(filename) and os.path.isfile(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                # Выводим текущее содержимое для редактирования
                for line in lines:
                    print(line, end="")
            except Exception as e:
                print(f"{RED}Error reading file:{RESET} {e}")

        # Цикл многострочного ввода
        while True:
            try:
                line = input()
                if line.strip() == ":q":
                    break
                lines.append(line + "\n")
            except (KeyboardInterrupt, EOFError):
                print("\nUse :q on a new line to save and exit.")
                break
        
        # Сохраняем изменения
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.writelines(lines)
            print(f"\n{GREEN}[+] File '{filename}' successfully saved!{RESET}\n")
        except Exception as e:
            print(f"\n{RED}Error saving file:{RESET} {e}\n")
    elif user_input.startswith("cat "):
        # Получаем имя файла (всё, что идет после "cat ")
        filename = user_input[4:].strip()
        
        if not filename:
            print("Error: Please specify a filename. Usage: cat [filename.txt]")
        else:
            # Проверяем, существует ли вообще такой файл
            if not os.path.exists(filename):
                print(f"Error: File '{filename}' does not exist.")
            # Проверяем, что это именно файл, а не папка
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
        # Получаем имя объекта для удаления
        target = user_input[3:].strip()
        
        if not target:
            print("Error: Please specify a file or directory to remove. Usage: rm [name]")
        elif not os.path.exists(target):
            print(f"Error: '{target}' does not exist.")
        else:
            try:
                # Если это папка
                if os.path.isdir(target):
                    # Проверяем, пустая ли папка, чтобы случайно не стереть лишнее
                    if not os.listdir(target):
                        os.rmdir(target)
                        print(f"Directory '{target}' successfully removed.")
                    else:
                        # Если не пустая, просим подтверждение
                        confirm = input(f"Directory '{target}' is not empty. Delete anyway? (y/n): ").strip().lower()
                        if confirm == 'y':
                            import shutil
                            shutil.rmtree(target)
                            print(f"Directory '{target}' and all its contents removed.")
                # Если это файл
                else:
                    os.remove(target)
                    print(f"File '{target}' successfully removed.")
            except Exception as e:
                print(f"Error: Could not remove '{target}'. Reason: {e}")
        # --- КОПИРОВАНИЕ (cp) ---
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
        filename = os.path.join(core_dir, "commands", "curl.py")

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
    elif user_input == "neofetch":
        script_dir = os.path.dirname(os.path.abspath(__file__))
        core_dir = os.path.dirname(script_dir)
        filename = os.path.join(core_dir, "commands", "neofetch.py")

        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    file_code = f.read()
            
            # Создаем изолированный контекст и передаем туда текущего юзера
                context = globals().copy()
                context["current_user"] = "root"  # Передаем имя авторизованного юзера
                context["VERSION"] = VERSION            # Передаем версию
            
                exec(file_code, context)
            except Exception as e:
                print(f"{RED}Error in neofetch:{RESET} {e}")
        else:
            print(f"{RED}FNF: {filename} not found{RESET}")
    elif user_input == "exit":
        sys.exit()
    elif not user_input:
        continue
    else:
        # Убираем лишние пробелы и кавычки, если пользователь их ввел
        clean_input = user_input.strip('"\'')
        # Проверяем, существует ли такой файл в текущей папке (куда мы перешли через cd)
        if os.path.exists(clean_input) and os.path.isfile(clean_input):
            print(f"Launching '{clean_input}' via system core...")
            launch_file(clean_input)
        else:
            print("Unknown command or file. Type 'help' to see available commands.")
    
