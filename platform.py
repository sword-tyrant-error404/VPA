# utils/platform.py — cross-platform OS helpers

import sys
import os
import subprocess
from pathlib import Path

PLATFORM = sys.platform  # 'linux', 'win32', 'darwin'


def open_camera():
    if PLATFORM == 'win32':
        os.system("start microsoft.windows.camera:")
    elif PLATFORM == 'linux':
        for app in ('cheese', 'guvcview', 'kamoso'):
            if subprocess.run(['which', app], capture_output=True).returncode == 0:
                subprocess.Popen([app])
                return
        print("No camera app found. Install cheese: sudo apt install cheese")
    elif PLATFORM == 'darwin':
        subprocess.Popen(['open', '-a', 'Photo Booth'])


def kill_camera():
    if PLATFORM == 'win32':
        os.system("taskkill /IM WindowsCamera.exe /F")
    elif PLATFORM == 'linux':
        for app in ('cheese', 'guvcview', 'kamoso'):
            os.system(f"pkill {app}")
    elif PLATFORM == 'darwin':
        os.system("pkill 'Photo Booth'")


def open_app(name: str):
    """Launch a desktop app by name string (from config.APPS)."""
    from config import APPS
    key = name.lower().strip()
    if key not in APPS:
        return False
    entry = APPS[key]
    plat = 'win' if PLATFORM == 'win32' else ('darwin' if PLATFORM == 'darwin' else 'linux')
    cmd = entry.get(plat, '')
    if not cmd:
        return False
    if PLATFORM == 'win32':
        os.system(cmd)
    else:
        subprocess.Popen(cmd.split())
    return True


def open_url(url: str):
    import webbrowser
    webbrowser.open(url)


def take_screenshot(filename: str = None):
    import time
    if filename is None:
        filename = f"screenshot_{time.strftime('%Y%m%d-%H%M%S')}.png"
    try:
        import pyautogui
        pyautogui.screenshot(filename)
        return filename
    except Exception as e:
        print(f"Screenshot error: {e}")
        return None


def vpa_root() -> Path:
    """Return the vpa/ root directory regardless of which script calls this."""
    return Path(__file__).resolve().parent.parent
