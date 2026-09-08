from pathlib import Path
from loaders.variables_loader import *
DEFAULT_COLORS = {
    "SQUARE": "\u2588",
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "MAGENTA": "\033[35m",
    "CYAN": "\033[36m",
    "WHITE": "\033[37m",
    "BLACK": "\033[30m",
    "BLUE": "\033[34m",
    "YELLOW": "\033[93m",
    "RESET": "\033[0m",
}
def _load_colors():
    colors = DEFAULT_COLORS.copy()
    current_file = Path(__file__).resolve() 
    loaders_dir = current_file.parent        
    pyos_dir = loaders_dir.parent            
    project_root = pyos_dir.parent          
    colors_file = project_root / "PS" / "configs" / "colors.cfg"
    try:
        with open(colors_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                value = value.replace('\\033', '\033').replace('\\u2588', '\u2588')
                if key in colors:
                    colors[key] = value
    except FileNotFoundError:
        print(f"{WARN}: file {colors_file} not found, using standart colours.")
    except Exception as e:
        print(f"{WARN}: error read colors.cfg ({e}). standart colours.")
    return colors
_colors = _load_colors()
SQUARE = _colors["SQUARE"]
RED = _colors["RED"]
GREEN = _colors["GREEN"]
MAGENTA = _colors["MAGENTA"]
CYAN = _colors["CYAN"]
WHITE = _colors["WHITE"]
BLACK = _colors["BLACK"]
BLUE = _colors["BLUE"]
YELLOW = _colors["YELLOW"]
RESET = _colors["RESET"]