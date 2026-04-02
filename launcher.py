# utils/launcher.py — fire-and-forget subprocess launcher

import sys
import subprocess
from pathlib import Path


def launch(script: str | Path, *args: str) -> subprocess.Popen:
    """
    Launch a child script in a completely separate process.
    Returns the Popen object so the caller can optionally wait/pipe.

    Usage:
        launch('games/tiktaktoe.py')
        launch('tools/alarm.py', 'set an alarm for 7 a.m.')
    """
    root = Path(__file__).resolve().parent.parent
    script_path = root / script
    cmd = [sys.executable, str(script_path)] + [str(a) for a in args]
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return proc


def launch_and_listen(script: str | Path, *args: str, speak_cb=None) -> subprocess.Popen:
    """
    Launch a child and stream its stdout back to a TTS callback.
    Lines prefixed with 'SPEAK:' are spoken; others are printed.

    Usage:
        launch_and_listen('tools/timer.py', command, speak_cb=talk1)
    """
    import threading

    proc = launch(script, *args)

    def _reader():
        for line in proc.stdout:
            line = line.rstrip()
            if line.startswith("SPEAK:") and speak_cb:
                speak_cb(line[6:].strip())
            elif line:
                print(f"[child] {line}")

    threading.Thread(target=_reader, daemon=True).start()
    return proc
