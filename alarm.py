#!/usr/bin/env python3
# tools/alarm.py — runs as its own process
# Usage: python alarm.py "set an alarm for 7:30 a.m."

import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import arrow
from pygame import mixer


def parse_alarm(inp: str) -> str:
    """Returns a time string like '7:30 AM' or '2:15 PM'."""
    inp = inp.lower()
    p1 = inp.find("alarm for")
    p2 = inp.find("a.m.")
    p3 = inp.find("p.m.")
    p4 = inp.find(":")

    base = inp[p1 + len("alarm for"):].strip() if p1 != -1 else inp

    if p2 != -1 and p4 != -1:
        t = inp[p1 + len("alarm for") + 1:p2].strip() + " AM"
    elif p3 != -1 and p4 != -1:
        t = inp[p1 + len("alarm for") + 1:p3].strip() + " PM"
    elif p2 != -1:
        t = inp[p1 + len("alarm for") + 1:p2].strip() + ":00 AM"
    elif p3 != -1:
        t = inp[p1 + len("alarm for") + 1:p3].strip() + ":00 PM"
    else:
        return ""
    return t.strip()


def run_alarm(inp: str):
    alarm_time = parse_alarm(inp)
    if not alarm_time:
        print("SPEAK: Could not understand alarm time.")
        sys.exit(1)

    print(f"SPEAK: Alarm set for {alarm_time}.")
    sys.stdout.flush()

    while True:
        now = arrow.now().format('h:mm A')
        if alarm_time.strip() == now.strip():
            print("SPEAK: Your alarm is going off!")
            sys.stdout.flush()
            try:
                root = Path(__file__).resolve().parent.parent
                alarm_file = root / 'alarm.wav'
                if alarm_file.exists():
                    mixer.init()
                    mixer.music.load(str(alarm_file))
                    mixer.music.play()
                    while mixer.music.get_busy():
                        time.sleep(1)
            except Exception as e:
                print(f"SPEAK: Alarm triggered! Could not play sound: {e}")
                sys.stdout.flush()
            break
        time.sleep(5)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("SPEAK: No alarm command provided.")
        sys.exit(1)
    run_alarm(' '.join(sys.argv[1:]))
