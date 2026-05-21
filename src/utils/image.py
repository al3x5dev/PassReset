import os
from pathlib import Path

# Constante a nivel módulo (se calcula una sola vez)
_ASSETS_DIR = Path(__file__).parent.parent / "assets"

def getImage(file: str) -> str:
    """Retorna ruta absoluta a un asset dentro de utils/assets/"""
    return str(_ASSETS_DIR / file)
