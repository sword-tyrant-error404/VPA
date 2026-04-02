#!/usr/bin/env python3
"""
VPA Post-Installation Verification Script
Checks that all dependencies and modules are correctly set up.
"""

import sys
import os
from pathlib import Path

print("=" * 50)
print("VPA Installation Verification")
print("=" * 50)

base_dir = Path(__file__).resolve().parent
errors = []
warnings = []

# Check required modules
print("\n1. Checking Python modules...")
required_modules = {
    'speech_recognition': 'SpeechRecognition',
    'pyttsx3': 'pyttsx3',
    'pywhatkit': 'pywhatkit',
    'pyautogui': 'pyautogui',
    'PIL': 'Pillow',
    'requests': 'requests',
    'bs4': 'beautifulsoup4',
    'yfinance': 'yfinance',
    'matplotlib': 'matplotlib',
    'pandas': 'pandas',
    'turtle': 'tkinter (usually pre-installed)',
    'gtts': 'gtts',
    'googletrans': 'googletrans',
}

for module, package in required_modules.items():
    try:
        __import__(module)
        print(f"  ✓ {module}")
    except ImportError as e:
        errors.append(f"  ✗ {module} - Install with: pip install {package}")
        print(f"  ✗ {module} (missing)")

# Check optional modules
print("\n2. Checking optional modules...")
optional_modules = {
    'wikipedia': 'wikipedia',
    'pyjokes': 'pyjokes',
    'vlc': 'python-vlc',
    'pydub': 'pydub',
}

for module, package in optional_modules.items():
    try:
        __import__(module)
        print(f"  ✓ {module}")
    except ImportError:
        warnings.append(f"  ⚠ {module} - Some features may not work. Install: pip install {package}")
        print(f"  ⚠ {module} (optional)")

# Check alarm sound file
print("\n3. Checking alarm sound file...")
alarm_file = base_dir / 'alarm.wav'
if alarm_file.exists():
    print(f"  ✓ alarm.wav found")
else:
    warnings.append("  ⚠ alarm.wav not found - timers and alarms will not play sound")
    print(f"  ⚠ alarm.wav missing (timers/alarms silent)")

# Check that main.py exists and can be parsed
print("\n4. Checking VPA structure...")
main_py = base_dir / 'main.py'
if main_py.exists():
    try:
        with open(main_py, 'r') as f:
            compile(f.read(), 'main.py', 'exec')
        print("  ✓ main.py syntax valid")
    except SyntaxError as e:
        errors.append(f"  ✗ main.py has syntax error: {e}")
        print(f"  ✗ main.py syntax error")
else:
    errors.append("  ✗ main.py not found")
    print("  ✗ main.py missing")

# Check that all module directories exist
for directory in ['games', 'tools', 'media', 'utils']:
    dir_path = base_dir / directory
    if dir_path.exists() and dir_path.is_dir():
        py_files = list(dir_path.glob('*.py'))
        print(f"  ✓ {directory}/ ({len(py_files)} modules)")
    else:
        errors.append(f"  ✗ {directory}/ directory missing")
        print(f"  ✗ {directory}/ missing")

# Check config.py
config_py = base_dir / 'config.py'
if config_py.exists():
    print("  ✓ config.py exists")
else:
    errors.append("  ✗ config.py missing")
    print("  ✗ config.py missing")

# Check launcher and TTS utilities
for util in ['utils/launcher.py', 'utils/tts.py']:
    if (base_dir / util).exists():
        print(f"  ✓ {util}")
    else:
        errors.append(f"  ✗ {util} missing")
        print(f"  ✗ {util} missing")

# Summary
print("\n" + "=" * 50)
print("SUMMARY")
print("=" * 50)

if errors:
    print("\n❌ CRITICAL ERRORS (must fix):")
    for error in errors:
        print(error)

if warnings:
    print("\n⚠️  WARNINGS (recommended fixes):")
    for warning in warnings:
        print(warning)

if not errors and not warnings:
    print("\n✅ Everything looks good! You can run:")
    print("   ./run_vpa.sh  (to test)")
    print("   ./setup_linux_service.sh  (to install as service)")
elif not errors:
    print("\n✅ Core functionality OK, but consider fixing warnings.")
else:
    print("\n❌ Please fix the errors above before running VPA.")

print("\n" + "=" * 50)
