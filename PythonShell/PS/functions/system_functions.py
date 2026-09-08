import sys
import time
import pywifi
from pywifi import const
import os
import re
import sys
import time
import platform
from datetime import datetime
from loaders.color_loader import *
from loaders import functions_loader as fl
from loaders.variables_loader import *
os_name = platform.system()
os_release = platform.release()
py_version = platform.python_version()
node_name = platform.node()    
cpu_name = fl.get_cpu_name()
used_ram, total_ram = fl.get_ram_info()
info = [
    f"{BLUE}@{node_name}{RESET}",
    "┌────────────────────────────────────────────┐",
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
            print(f"{RED}Canceled.{RESET}")
            pass
    elif note.startswith("-t"):
        note_text = note[2:].strip()
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
        raw_info = [
            f"{BLUE}@{node_name}{RESET}",
            f"{YELLOW}OS{RESET}       : {os_name} {os_release}",
            f"{YELLOW}PY-shell{RESET} : {VERSION}",
            f"{YELLOW}Python{RESET}   : {py_version}",
            f"{YELLOW}CPU{RESET}      : {cpu_name}",
            f"{YELLOW}RAM{RESET}      : {used_ram} / {total_ram}",
            f"{YELLOW}Creator{RESET}  : https://github.com/HayaraLV",
            "",
            f"{BLACK}{SQUARE}{SQUARE}{RESET}{SQUARE}{SQUARE}{RED}{SQUARE}{SQUARE}{GREEN}{SQUARE}{SQUARE}{YELLOW}{SQUARE}{SQUARE}{BLUE}{SQUARE}{SQUARE}{MAGENTA}{SQUARE}{SQUARE}{RESET}{CYAN}{SQUARE}{SQUARE}{RESET}",
        ]
        def get_visible_len(text):
            return len(re.sub(r'\033\[\d+(;\d+)*m', '', text))
        max_len = max(get_visible_len(line) for line in raw_info)
        padding = 2
        content_width = max_len + padding
        info = []
        info.append(f"{YELLOW}┌{RESET}" + f"{YELLOW}─{RESET}" * (content_width + 2) + f"{YELLOW}┐{RESET}")
        for line in raw_info:
            spaces = content_width - get_visible_len(line)
            info.append(f"{YELLOW}│{RESET} {line}{' ' * spaces} {YELLOW}│{RESET}")
        info.append(f"{YELLOW}└{RESET}" + f"{YELLOW}─{RESET}" * (content_width + 2) + f"{YELLOW}┘{RESET}")
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
        TERMINAL_HISTORY.clear()
    elif args == "-h":
        print("Arguments:")
        print("    -h -> Show this owerview.")
        print("    -c -> Clear command history.")
    elif args == "":
        if not TERMINAL_HISTORY:
            print("History is empty.")
        for index, cmd in enumerate(TERMINAL_HISTORY, 1):
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
    clean_args = args.strip() if args else ""
    target_path = Path(clean_args) if clean_args else Path(".")    
    if target_path.exists() and target_path.is_dir():
        absolute_path = target_path.resolve()        
        print(f"{RESET}{absolute_path}")
        print("│")        
        fl.print_tree(absolute_path)
    else:
        print(f"{ERR} The specified path does not exist or is not a folder.")
def cd_command(args):
    target_dir = args.strip()
    if not target_dir:
        print(f"{BLUE}Usage: cd [directory_name]{RESET}")
    else:
        try:
            os.chdir(target_dir)
        except Exception as e:
            print(f"{ERR} {e}")
def mkdir_command(args):
    folder_name = args.strip()
    if not folder_name:
        folder_name = input("Enter new directory name: ").strip()
    if not folder_name:
        fl.slowprint(f"{ERR} Directory name cannot be empty.{RESET}")
    else:
        try:
            os.makedirs(folder_name)
            fl.slowprint(f"{GREEN}Directory{RESET} '{folder_name}' {GREEN}successfully created.{RESET}")
        except FileExistsError:
            fl.slowprint(f"{ERR} Directory '{folder_name}' {YELLOW}already exists.{RESET}")
        except Exception as e:
            fl.slowprint(f"{ERR} Could not create directory. {RESET}Reason: {e}")
def touch_command(args):
    filename = args.strip()
    if not filename:
        print("{ERR} Please specify a filename. Usage: touch [filename.txt]")
    else:
        try:
            with open(filename, 'a', encoding='utf-8') as f:
                pass
            print(f"Created file: {filename}")
        except Exception as e:
            print(f"{ERR} Could not create file. Reason: {e}")
def cat_command(args):
    filename = args.strip()
    if not filename:
        print("{ERR} Please specify a filename. Usage: cat [filename.txt]")
    else:
        if not os.path.exists(filename):
            print(f"{ERR} File '{filename}' does not exist.")
        elif os.path.isdir(filename):
            print(f"{ERR} '{filename}' is a directory, not a file.")
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
                print(f"{ERR} Could not read file. Reason: {e}")
def edit_command(args):
    filename = args.strip()
    if not filename:
        print(f"{ERR} Please specify a file name. Usage: edit [file_name]{RESET}")
        return
    print(f"\033[34m=== Shell Text Editor ===\033[0m")
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
            print(f"{ERR} reading file:{RESET} {e}")
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
        print(f"\n{RED}{ERR} saving file:{RESET} {e}\n")
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
            print(f"{ERR} writing to file: {e}")
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
            print(f"{ERR} {e}")
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
            print(f"{ERR} {e}")
    else:
        print(f"{RED}Usage: mv [source] [destination]{RESET}")
def rm_command(args):
    target = args.strip()
    if not target:
        print("{ERR} Please specify a file or directory to remove. Usage: rm [name]")
    elif not os.path.exists(target):
        print(f"{ERR} '{target}' does not exist.")
    else:
        try:
            if os.path.isdir(target):
                if not os.listdir(target):
                    os.rmdir(target)
                    print(f"Directory '{target}' successfully removed.")
                else:
                    confirm = input(f"Directory '{target}' is {RED}not{RESET} empty. Delete anyway? (Y/n): ").strip().lower()
                    if confirm == 'Y':
                        fl.shutil.rmtree(target)
                        print(f"Directory '{target}' and all its contents removed.")
            else:
                confirm = input(f"{RED}Delete{RESET} {BLUE}{target}{RESET} (Y/n): ")
                if confirm == 'Y':
                    os.remove(target)
                    print(f"File '{target}' successfully removed.")
        except Exception as e:
            print(f"{ERR} Could not remove -> '{YELLOW}{target}{RESET}'. Reason: {e}")
def grep_command(args):
    keywords = args.strip().split()
    if keywords:
        found = False       
        for item in os.listdir('.'):
            if os.path.isfile(item):
                try:
                    with open(item, 'r', encoding='utf-8') as f:
                        for idx, line in enumerate(f, 1):
                            clean_line = line.strip()
                            line_matched = False                            
                            for word in keywords:
                                if word in clean_line:
                                    clean_line = clean_line.replace(word, f"{RED}{word}{RESET}")
                                    line_matched = True                            
                            if line_matched:
                                print(f"{BLUE}{item}:{idx}{RESET} {YELLOW}->{RESET} {clean_line}")
                                found = True
                except:
                    pass
        if not found:
            search_str = " ".join(keywords)
            print(f"{YELLOW}No matches found for{RESET} '{BLUE}{search_str}{RESET}'")
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
        elif sys_name == "Windows" and ext not in [".py", ".exe", ".bat", ".lnk"]:
            print(f"{ERR} Windows core cannot run '{ext}' files via this command.{RESET}")
            print(f"{YELLOW}Allowed formats: .py, .exe, .bat, .lnk{RESET}")
            return
        elif sys_name in ["Linux", "Darwin"] and ext not in [".py", ".sh", ""]:
            print(f"{ERR} Unix environment cannot run '{ext}' files.{RESET}")
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
            print(f"{ERR} while executing the script:{RESET} {e}")
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
            print(f"{ERR} in curl:{RESET} {e}")
    else:
        print(f"{RED}FNF: {filename} not found{RESET}")
def ping_command(args):
    cmd_args = args.strip()
    fl.check_site(cmd_args)

class WiFiState:
    def __init__(self):
        self.wifi = pywifi.PyWiFi()
        interfaces = self.wifi.interfaces()
        self.iface = interfaces[0] if interfaces else None
        self.found_networks = []
wifi_state = WiFiState()
def wifi_command(args):
    wifi_args = args.strip()
    
    if not wifi_state.iface:
        print(f"{ERR} Wi-Fi adapter {RED}not{RESET} found in the system.")
        return
    parts = wifi_args.split()
    if not parts:
        print("Usage: wifi [-l | -c [num] | -d]")
        return

    flag = parts[0]

    if flag == "-l":
        print("Scan Wi-Fi networks...")
        wifi_state.iface.scan()
        time.sleep(2)
        
        raw_results = wifi_state.iface.scan_results()
        seen_ssids = set()
        wifi_state.found_networks = []
        
        for net in raw_results:
            ssid = net.ssid.strip()
            if ssid and ssid not in seen_ssids:
                seen_ssids.add(ssid)
                wifi_state.found_networks.append(net)
        
        if not wifi_state.found_networks:
            print("Aviable networks not found.")
            return
            
        print("\nAviable networks:")
        for index, net in enumerate(wifi_state.found_networks, start=1):
            signal = net.signal
            if signal < 0:
                signal = max(0, min(100, 2 * (signal + 100)))
            print(f" [{index}] {net.ssid} (Signal: {signal}%)")

    elif flag == "-c":
        if len(parts) < 2:
            print(f"{ERR} Enter number of network. Example: wifi -c 2")
            return
            
        if not wifi_state.found_networks:
            print(f"{ERR} Firsts search for networks using 'wifi -l'")
            return
            
        try:
            idx = int(parts[1]) - 1
            if idx < 0 or idx >= len(wifi_state.found_networks):
                print(f"{ERR} Invalid number. Available: 1-{len(wifi_state.found_networks)}")
                return
        except ValueError:
            print(f"{ERR} Number of network must be a number.")
            return
            
        target_net = wifi_state.found_networks[idx]
        password = input(f"Enter password for: {target_net.ssid}: ")
        
        print(f"Connecting to {target_net.ssid}...")
        
        import platform
        import subprocess
        current_os = platform.system()
        
        if current_os == "Linux":
            try:
                result = subprocess.run(
                    ["nmcli", "dev", "wifi", "connect", target_net.ssid, "password", password],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    print(f"Successfully connected to the network {target_net.ssid}!")
                else:
                    print(f"{ERR} Failed to connect:\n{result.stderr.strip()}")
            except Exception as e:
                print(f"{ERR} Error calling system utility: {e}")
                
        elif current_os == "Windows":
            wifi_state.iface.disconnect()
            time.sleep(1)
            
            profile = pywifi.Profile()
            profile.ssid = target_net.ssid
            profile.auth = const.AUTH_ALG_OPEN
            profile.akm.append(const.AKM_TYPE_WPA2PSK)
            profile.cipher = const.CIPHER_TYPE_CCMP
            profile.key = password
            
            wifi_state.iface.remove_all_network_profiles()
            tmp_profile = wifi_state.iface.add_network_profile(profile)
            wifi_state.iface.connect(tmp_profile)
            
            connected = False
            for _ in range(5):
                time.sleep(1)
                if wifi_state.iface.status() == const.IFACE_CONNECTED:
                    connected = True
                    break
                    
            if connected:
                print(f"Successfully connected to the network: {target_net.ssid}")
            else:
                print(f"{ERR} Unable to connect. Check the password.")

    elif flag == "-d":
        print("Disconnecting...")
        import platform
        import subprocess

        try:
            wifi_state.iface.disconnect()
            time.sleep(1)
        except Exception:
            pass

        current_os = platform.system()
        try:
            if current_os == "Linux":
                cmd_iface = subprocess.run(["nmcli", "-t", "-f", "DEVICE,TYPE", "device"], capture_output=True, text=True)
                wifi_dev = "wlan0"
                for line in cmd_iface.stdout.strip().split("\n"):
                    if ":wifi" in line:
                        wifi_dev = line.split(":")[0]
                        break
                
                subprocess.run(["nmcli", "device", "disconnect", wifi_dev], capture_output=True)
                
            elif current_os == "Windows":
                subprocess.run(["netsh", "wlan", "disconnect"], capture_output=True)
                
            print("Отключение успешно выполнено.")
        except Exception as e:
            print(f"[Ошибка] Не удалось принудительно отключить Wi-Fi: {e}")
        
    else:
        print(f"[Ошибка] Неизвестный флаг: {flag}. Используйте -l, -c или -d")

