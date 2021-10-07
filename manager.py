import os
import sys

def get_absolut_path(relpath):
    """
        Reperage de dossier de travaille a partir d'un module
    """
    workspace = os.path.dirname(__file__)
    if not os.path.exists(os.path.join(workspace, relpath)):
        workspace = os.path.dirname(workspace)
    absPath = os.path.join(workspace, relpath)
    return absPath

def rgb_to_hex(rgb):
    try:
        return '#%02x%02x%02x' % rgb
    except Exception:
        return False

def hex_to_rgb(hexa):
    try:
        hexa = hexa.lstrip('#')
        lv = len(hexa)
        return tuple(int(hexa[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    except Exception:
        return False
