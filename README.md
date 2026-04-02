# VPA (Virtual Personal Assistant) - Linux Setup Guide

Your VPA is modular and ready to be deployed as a Linux background service!

## Quick Start

### 1. Test Manually First
```bash
cd /home/bayazid/vpa_env/VPA
./run_vpa.sh
```
This runs the assistant in your current terminal. Say "alexa" and give commands.

### 2. Install as Systemd Service

Run the automated setup script:
```bash
./setup_linux_service.sh
```

Follow the instructions printed. Typically:
```bash
sudo cp /tmp/vpa.service /etc/systemd/system/vpa.service
sudo systemctl daemon-reload
sudo systemctl enable vpa.service
sudo systemctl start vpa.service
```

### 3. Check Status & Logs
```bash
# Check if service is running
sudo systemctl status vpa.service

# View logs in real-time
sudo journalctl -u vpa.service -f
```

### 4. Manage the Service
```bash
# Stop the service
sudo systemctl stop vpa.service

# Start the service
sudo systemctl start vpa.service

# Restart the service
sudo systemctl restart vpa.service

# Disable from starting on boot
sudo systemctl disable vpa.service
```

## Required Permissions

The service needs access to:

1. **Microphone** (for voice recognition):
   ```bash
   sudo usermod -a -G audio $USER
   ```

2. **Camera** (for "show me" command):
   ```bash
   sudo usermod -a -G video $USER
   ```

3. **Display/GUI** (for games, matplotlib plots, etc.):
   - You need an X11 or Wayland session running
   - The service must have access to your display

**After running the above commands, log out and log back in** for group changes to take effect.

## Environment Notes

The service file sets these environment variables:
- `DISPLAY=:0` - for GUI applications
- `XAUTHORITY` - for X11 authentication
- `PULSE_SERVER` - for PulseAudio sound
- `XDG_RUNTIME_DIR` - for user runtime files

If you use Wayland instead of X11, you may need to adjust the service.

## Troubleshooting

### Microphone not working?
Check if your user is in the `audio` group:
```bash
groups $USER
```
If not, add and re-login.

### No sound output?
Test with:
```bash
speaker-test -c 2 -t wav
```

### Permission denied on /dev/video0?
Add user to `video` group and re-login.

### Service fails to start?
Check logs:
```bash
sudo journalctl -u vpa.service -n 50 --no-pager
```

Common issues:
- Missing dependencies: `pip install -r requirements.txt`
- Wrong Python path in service file
- Display not set (ensure you're logged into a desktop session)

### GUI apps won't open?
The service needs access to your X/Wayland session. When testing, make sure:
- You're logged into a desktop environment (GNOME, KDE, XFCE, etc.)
- `echo $DISPLAY` shows something like `:0` or `:1`
- `xhost +SI:localuser:$USER` allows local users to connect to X server

## Dependencies

Install all Python dependencies:
```bash
cd /home/bayazid/vpa_env/VPA
source venv/bin/activate  # if using venv
pip install speechrecognition pyttsx3 pywhatkit pyautogui \
  pygame tkinter pyjokes arrow requests beautifulsoup4 gtts pydub \
  googletrans pillow yfinance matplotlib pandas vlc wikipedia
```

Also install system packages:
```bash
# Ubuntu/Debian
sudo apt install python3-pip python3-dev portaudio19-dev \
  ffmpeg libsndfile1 pulseaudio-utils

# Fedora
sudo dnf install python3-pip portaudio-devel ffmpeg
```

## How It Works

The VPA:
1. Starts TTS worker thread
2. Listens for the wake word "alexa"
3. Recognizes voice commands
4. Dispatches to appropriate modules:
   - Games → launches games/ subprocess
   - Tools (timer, alarm, email, etc.) → launches tools/ subprocess
   - Media (stock, crypto, news) → launches media/ subprocess
   - Utilities (open apps, web search) → handled directly
5. Speaks responses via TTS (queue-based for thread safety)

## Configuration

Edit `config.py` to customize:
- `EMAILS` dictionary (student emails)
- `APPS` and `WEB_APPS` (app launcher commands)
- `EMAIL_SENDER` (for sending emails)

## Uninstall

To remove the service:
```bash
sudo systemctl stop vpa.service
sudo systemctl disable vpa.service
sudo rm /etc/systemd/system/vpa.service
sudo systemctl daemon-reload
```

## Notes

- The service runs as your user (not root) for security
- All GUI apps (games, matplotlib, etc.) open on your active desktop
- If you're not logged into a desktop session, GUI features won't work
- Voice recognition requires an internet connection (Google Speech API)
- The assistant runs forever until stopped or system shuts down

Enjoy your always-on personal assistant!
