import os
import sys
import time
import platform
from datetime import datetime
from loaders.color_loader import *
from loaders import functions_loader as fl
from loaders import variables_loader as vr
os_name = platform.system()
os_release = platform.release()
py_version = platform.python_version()
node_name = platform.node()    
cpu_name = fl.get_cpu_name()
used_ram, total_ram = fl.get_ram_info()
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
def date_command(args):
    if not args:
        now = datetime.now()
        formatted_date = now.strftime("%Y.%m.%d | %H:%M:%S")
        print(formatted_date)
    else:
        if args.startswith("-h"):
            print(f"{BLUE}Arguments [help]:{RESET}")
            print(f"{YELLOW}    -h {RESET}->{BLUE} Show this owerview{RESET}")
            print(f"{YELLOW}    -f {RESET}->{BLUE} Write the current date to a file{RESET}")
        if args.startswith("-f"):
            formatted_date = datetime.now().strftime("%Y.%m.%d | %H:%M:%S")
            filename = "datetime.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(formatted_date)
                current_dir = os.path.basename(os.getcwd())
                print(f"Written to -> {filename} | directory -> {current_dir}")

def note_command(args):
    note = args.strip()
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
        note_text = note[2:].strip()  # после "-t"
        with open(notes_filename, 'a', encoding='utf-8') as f:
            f.write(datetime.now().strftime("%Y.%m.%d | %H:%M:%S") + "\n")
            f.write(note_text + "\n\n")
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
    elif note not in ["-c", "-t", "-h", "-r"]:
        with open(notes_filename, 'a', encoding='utf-8') as f:
            f.write(note + "\n\n")
        print(f"{GREEN}Writed{RESET} -> {notes_filename}")

def clear_command(args):
    os.system('cls' if os.name == 'nt' else 'clear')

def sys_command(args):
    if not args:
        print("Try sys -i || sys -h")
    elif args == "-i":
        logo_dir = os.path.dirname(os.path.abspath(__file__))
        core_dir = os.path.dirname(logo_dir)
        logo_filename = os.path.join(core_dir, "configs", "logo.cfg")
        with open(logo_filename, 'r', encoding='utf-8') as file:
            logo_code = file.read()
        logo_namespace = {}
        exec(logo_code, logo_namespace)
        logo = logo_namespace.get('logo', [])
        print()
        for i in range(max(len(logo), len(info))):
            logo_line = logo[i] if i < len(logo) else " " * 40
            info_line = info[i] if i < len(info) else ""
            print(f" {logo_line}  {info_line}")
        print()
    elif args == "-h":
        print(f"{BLUE}Arguments:{RESET}")
        print(f"    -i -> {YELLOW}Show system info.{RESET}")
        print(f"    -h -> {YELLOW}Show this owerview.{RESET}")

def history_command(args):
    global TERMINAL_HISTORY
    if args == "-c":
        vr.TERMINAL_HISTORY.clear()
    elif args == "-h":
        print("Arguments:")
        print("    -h -> Show this owerview.")
        print("    -c -> Clear command history.")
    elif args == "":
        if not vr.TERMINAL_HISTORY:
            print("История пуста.")
        for index, cmd in enumerate(vr.TERMINAL_HISTORY, 1):
            print(f" {index}  {cmd}")
    else:
        print(f"Unknown argument. Use 'history' or 'history -c'")

def exit_command(args):
    sys.exit()

def ls_command(args):
    files = os.listdir('.')
    if not files:
        fl.slowprint(f"{RED}Directory is empty.{RESET}")
    else:
        fl.slowprint("\nContents of current directory:")
        for item in files:
            if os.path.isdir(item):
                fl.slowprint(f"  [DIR]  {item}")
            else:
                fl.slowprint(f"  [FILE] {item}")
        print()

def tree_command(args):
    target_path = Path(args) if args else Path(".")
    if target_path.exists() and target_path.is_dir():
        print(target_path.name)
        fl.print_tree(target_path)
    else:
        print("Error: The specified path does not exist or is not a folder.")

def cd_command(args):
    target_dir = args.strip()
    if not target_dir:
        print(f"{BLUE}Usage: cd [directory_name]{RESET}")
    else:
        try:
            os.chdir(target_dir)
        except Exception as e:
            print(f"{RED}Error:{RESET} {e}")

def mkdir_command(args):
    folder_name = args.strip()
    if not folder_name:
        folder_name = input("Enter new directory name: ").strip()
    if not folder_name:
        fl.slowprint(f"{RED}Error: Directory name cannot be empty.{RESET}")
    else:
        try:
            os.makedirs(folder_name)
            fl.slowprint(f"{GREEN}Directory{RESET} '{folder_name}' {GREEN}successfully created.{RESET}")
        except FileExistsError:
            fl.slowprint(f"{YELLOW}Error: Directory{RESET} '{folder_name}' {YELLOW}already exists.{RESET}")
        except Exception as e:
            fl.slowprint(f"{RED}Error: Could not create directory. {RESET}Reason: {e}")

def touch_command(args):
    filename = args.strip()
    if not filename:
        print("Error: Please specify a filename. Usage: touch [filename.txt]")
    else:
        try:
            with open(filename, 'a', encoding='utf-8') as f:
                pass
            print(f"Created file: {filename}")
        except Exception as e:
            print(f"Error: Could not create file. Reason: {e}")

def cat_command(args):
    filename = args.strip()
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
                    print(content)
                    print("-------------------------\n")
            except Exception as e:
                print(f"Error: Could not read file. Reason: {e}")

def edit_command(args):
    filename = args.strip()
    if not filename:
        print(f"{RED}Error: Please specify a file name. Usage: edit [file_name]{RESET}")
        return
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

def echo_command(args):
    raw_content = args.strip()
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

def cp_command(args):
    parts = args.strip().split(" ")
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

def mv_command(args):
    parts = args.strip().split(" ")
    if len(parts) >= 2:
        src, dst = parts[0], parts[1]
        try:
            os.rename(src, dst)
            print(f"{GREEN}Successfully moved/renamed to {dst}{RESET}")
        except Exception as e:
            print(f"{RED}Error:{RESET} {e}")
    else:
        print(f"{RED}Usage: mv [source] [destination]{RESET}")

def rm_command(args):
    target = args.strip()
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
                        fl.shutil.rmtree(target)
                        print(f"Directory '{target}' and all its contents removed.")
            else:
                confirm = input(f"Delete {target} (Y/n): ")
                if confirm == 'Y':
                    os.remove(target)
                    print(f"File '{target}' successfully removed.")
        except Exception as e:
            print(f"Error: Could not remove '{target}'. Reason: {e}")

def grep_command(args):
    keyword = args.strip()
    if keyword:
        found = False
        for item in os.listdir('.'):
            if os.path.isfile(item) and (item.endswith('.py') or item.endswith('.txt')):
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

def run_command(args):
    raw_path = args.strip()
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
            return
        elif sys_name == "Windows" and ext not in [".py", ".exe", ".bat", ".cmd", ".lnk"]:
            print(f"{RED}Error: Windows core cannot run '{ext}' files via this command.{RESET}")
            print(f"{YELLOW}Allowed formats: .py, .exe, .bat, .cmd, .lnk{RESET}")
            return
        elif sys_name in ["Linux", "Darwin"] and ext not in [".py", ".sh", ""]:
            print(f"{RED}Error: Unix environment cannot run '{ext}' files.{RESET}")
            return
        print(f"\033[34m[Launch {filename}...]\033[0m")
        try:
            if ext == ".py":
                with open(filename, "r", encoding="utf-8") as f:
                    file_code = f.read()
                sandbox_globals = globals().copy()
                sandbox_globals["current_user"] = "root"
                sandbox_globals["VERSION"] = VERSION
                sandbox_locals = {}
                exec(file_code, sandbox_globals, sandbox_locals)
            elif sys_name == "Windows" and ext == ".lnk":
                fl.subprocess.run(f'start "" "{filename}"', shell=True, check=True)
            else:
                if sys_name == "Windows":
                    fl.subprocess.run(f'"{filename}"', shell=True, check=True)
                else:
                    if not os.access(filename, os.X_OK):
                        os.chmod(filename, 0o755)
                    fl.subprocess.run([filename], check=True)
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

def curl_command(args):
    cmd_args = args.strip()
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
def ping_command(args):
    cmd_args = args.strip()
    fl.check_site(cmd_args)
