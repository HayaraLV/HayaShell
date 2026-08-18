import sys
RED = "\033[31m"
GREEN = "\033[32m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
BLACK = "\033[30m"
BLUE = "\033[34m"
YELLOW = "\033[93m"
RESET = "\033[0m"

commands = {
    f"{YELLOW}help{RESET}": "Show this overview",
    f"{YELLOW}clear{RESET}": "Clear the terminal screen",
    f"{YELLOW}ls{RESET}": "List directory contents",
    f"{YELLOW}tree{RESET}": "Tree of directory contents",
    f"{YELLOW}cd{RESET}": f"Change current directory {BLUE}(Usage: cd [directory_name]){RESET}",
    f"{YELLOW}mkdir{RESET}": "Create a new directory",
    f"{YELLOW}touch{RESET}": f"Create a new empty file {BLUE}(Usage: touch [file_name]){RESET}",
    f"{YELLOW}cat{RESET}": f"Read and display file contents {BLUE}(Usage: cat [file_name]){RESET}",
    f"{YELLOW}edit{RESET}": f"Open text editor to modify a file {BLUE}(Usage: edit [file_name]){RESET}",
    f"{YELLOW}echo{RESET}": f"Write text to file {BLUE}(Usage: echo [text] > [file_name]){RESET}",
    f"{YELLOW}cp{RESET}": f"Copy a file or directory {BLUE}(Usage: cp [source] [destination]){RESET}",
    f"{YELLOW}mv{RESET}": f"Move or rename a file or directory {BLUE}(Usage: mv [source] [destination]){RESET}",
    f"{YELLOW}rm{RESET}": f"Remove a file or a directory {BLUE}(Usage: rm [file_name]){RESET}",
    f"{YELLOW}grep{RESET}": f"Search for text pattern inside files {BLUE}(Usage: grep [text]){RESET}",
    f"{YELLOW}run{RESET}": f"Execute files and scripts {BLUE}(Usage: run [file_name]){RESET}",
    f"{YELLOW}neofetch{RESET}": "Show system information and logo",
    f"{YELLOW}curl{RESET}": f"Download files from the internet via URL {BLUE}(Usage: curl [url] [output_name]){RESET}",
    f"{YELLOW}history{RESET}": f"Show command history {BLUE}(Usage: history [-c to clear]){RESET}",
    f"{YELLOW}exit{RESET}": "Shutdown the system"
}

print("\nAvailable commands:")
for cmd, desc in commands.items():
    print(f"  {cmd:<20} - {desc}")
print()
