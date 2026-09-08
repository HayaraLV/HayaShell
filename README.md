## Python Shell by HayaraLV

![logo_image](images/image.png)


A custom shell written in Python.

## Features

###  File System & Navigation
* **`cd`** — Change the current working directory.
* **`ls`** — List directory contents.
* **`tree`** — Display directory structure in a visual tree format.
* **`mkdir`** — Create new directories.

###  File & Text Management
* **`touch`** — Create new empty files.
* **`cat`** — Concatenate and display file content.
* **`edit`** — In-terminal text editing utility.
* **`echo`** — Print text or redirect output to a file.
* **`note`** — Quick note-taking tool.
* **`cp`** — Copy files and directories.
* **`mv`** — Move or rename files and directories.
* **`rm`** — Remove files and directories.
* **`grep`** — Search for specific patterns within text.

###  Networking & Execution
* **`curl`** — Send basic network and HTTP requests.
* **`ping`** — Check network host connectivity.

###  System & Environment
* **`sys`** — Display brief technical system information.
* **`neofetch`** — Visual, detailed system information layout.
* **`date`** — Show current date and time.
* **`run`** — Execute external system commands.
* **`clear`** — Clear the terminal screen.

###  Terminal Control
* **`help`** — Show the list of available commands and usage instructions.
* **`history`** — View the command execution history.
* **`exit`** — Safely close the terminal session.

###  Core Architecture
* **Custom Command Parser** — Custom-built logic for robust command and argument handling.
* **Cross-Platform Implementation** — Fully written in Python to ensure seamless compatibility across Windows, macOS, and Linux.


## Available Commands

![helpfull](images/helpfull.png)

## How to Run

This program can be executed on Linux, Windows, and macOS. Depending on your operating system, use the appropriate commands below.

### Linux
The script requires superuser privileges (`sudo`) to function correctly on Linux:
```bash
sudo /usr/bin/python3 /PythonShell/PS/PyShell.py
```
Alternatively, navigate to the project directory and run:
```bash
cd PythonShell/PS/
sudo python3 PyShell.py
```

### Windows
On Windows, use the standard `python` interpreter (or `py` launcher) and backslashes `\` for paths.

**Standard execution:**
```cmd
python "C:\PythonShell\PS\PyShell.py"
```

**With Administrator privileges:**
1. Open **Command Prompt** or **PowerShell** as Administrator.
2. Execute the following commands:
```cmd
cd "C:\PythonShell\PS"
python PyShell.py
```

### macOS
macOS uses a Unix path structure where the user's home directory is located under `/Users/`.

```bash
sudo python3 /PythonShell/PS/PyShell.py
```
Alternatively, navigate to the project directory and run:
```bash
cd /PythonShell/PS
sudo python3 PyShell.py
```


## Version

Current version: 2.0.0.0

## About

A lightweight, cross-platform custom shell written in Python. It replicates core Unix terminal functionality with built-in navigation, file management, basic networking, and system utilities.
