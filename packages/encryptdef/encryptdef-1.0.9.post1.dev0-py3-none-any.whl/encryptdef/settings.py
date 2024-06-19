"""Módulo que contém as configurações da ferramenta"""

import os

from rich.console import Console
from rich.theme import Theme

CURRENT_DIR = os.getcwd()

CUSTOM_THEME = Theme(
    {
        "critical": "bold red",
        "error": "bold red",
        "warning": "bold yellow",
        "info": "bold cyan",
        "debug": "bold green",
    }
)
console = Console(theme=CUSTOM_THEME)
