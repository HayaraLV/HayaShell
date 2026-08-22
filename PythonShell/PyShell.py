from loaders.color_loader import *
from loaders import functions_loader as fl
from loaders import variables_loader as vr
import os
from datetime import datetime
from pathlib import Path
commands = {
    "help": fl.help_command,
    "date": fl.date_command,
    "note": fl.note_command,
    "clear":fl.clear_command,
    "sys": fl.sys_command,
    "history": fl.history_command,
    "exit": fl.exit_command,
    "ls": fl.ls_command,
    "tree": fl.tree_command,
    "cd": fl.cd_command,
    "mkdir": fl.mkdir_command,
    "touch": fl.touch_command,
    "cat": fl.cat_command,
    "edit": fl.edit_command,
    "echo": fl.echo_command,
    "cp": fl.cp_command,
    "mv": fl.mv_command,
    "rm": fl.rm_command,
    "grep": fl.grep_command,
    "run": fl.run_command,
    "curl": fl.curl_command,
    "ping": fl.ping_command,
}
fl.slowprint(f"Type '{BLUE}help{RESET}' to see a list of available commands.\n")
while True:
    current_dir = os.getcwd()
    if not current_dir:
        current_dir = "/"
    user_input = input(f"{YELLOW}{vr.ROOT_NAME}{BLUE}@py-shell:{RESET}{current_dir}{BLUE}:~${RESET} ").strip()
    if not user_input:
        continue
    cmd_name = user_input.split()[0]
    if cmd_name != "history" and cmd_name != "exit":
        vr.TERMINAL_HISTORY.append(user_input)
    parts = user_input.split(maxsplit=1)
    cmd = parts[0]
    args = parts[1] if len(parts) > 1 else ""
    if cmd in commands:
        commands[cmd](args)
    else:
        clean_input = user_input.strip('"\'')
        if os.path.exists(clean_input) and os.path.isfile(clean_input):
            print(f"Launching '{clean_input}' via system core...")
            fl.launch_file(clean_input)
        else:
            print("Unknown command or file. Type 'help' to see available commands.")
