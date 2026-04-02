#!/bin/bash
# VPA Linux Service Setup Script
# Run this to install VPA as a systemd service

set -e

echo "=========================================="
echo "VPA Linux Service Setup"
echo "=========================================="

# Get current user
CURRENT_USER=$(whoami)
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_PYTHON="$PROJECT_DIR/venv/bin/python"

# Check if virtual environment exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "ERROR: Virtual environment not found at $PROJECT_DIR/venv/bin/python"
    echo "Please ensure you have a virtual environment set up."
    exit 1
fi

# Check dependencies
echo "Checking dependencies..."
DEPS=("speech-recognition" "pyttsx3" "pywhatkit" "pyautogui" "pillow" "requests" "yfinance" "matplotlib" "pandas" "vlc" "wikipedia")
for dep in "${DEPS[@]}"; do
    if ! python3 -c "import $(echo $dep | tr '-' '_')" 2>/dev/null; then
        echo "WARNING: $dep may not be installed. Run: pip install $dep"
    fi
done

# Create service file with actual paths
SERVICE_FILE="/tmp/vpa.service"
cat > "$SERVICE_FILE" << EOF
[Unit]
Description=Virtual Personal Assistant (VPA)
After=network.target sound.target multi-user.target

[Service]
Type=simple
User=$CURRENT_USER
Group=$CURRENT_USER
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin"
Environment="PYTHONPATH=$PROJECT_DIR"
Environment="DISPLAY=:0"
Environment="XAUTHORITY=/home/$CURRENT_USER/.Xauthority"
Environment="PULSE_SERVER=unix:/run/user/$(id -u $CURRENT_USER)/pulse/native"
Environment="XDG_RUNTIME_DIR=/run/user/$(id -u $CURRENT_USER)"
ExecStart=$VENV_PYTHON $PROJECT_DIR/main.py
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

echo ""
echo "Service file created at: $SERVICE_FILE"
echo ""
echo "To install the service:"
echo "  1. Copy the service file: sudo cp $SERVICE_FILE /etc/systemd/system/vpa.service"
echo "  2. Reload systemd: sudo systemctl daemon-reload"
echo "  3. Enable on boot: sudo systemctl enable vpa.service"
echo "  4. Start service: sudo systemctl start vpa.service"
echo "  5. Check status: sudo systemctl status vpa.service"
echo "  6. View logs: sudo journalctl -u vpa.service -f"
echo ""
echo "IMPORTANT: For microphone access, you need:"
echo "  - Add your user to the 'audio' group: sudo usermod -a -G audio $CURRENT_USER"
echo "  - For camera access, add to 'video' group: sudo usermod -a -G video $CURRENT_USER"
echo "  - Log out and back in for group changes to take effect."
echo ""
echo "To stop the service: sudo systemctl stop vpa.service"
echo "To disable on boot: sudo systemctl disable vpa.service"
echo ""
echo "Testing first:"
echo "  You can test manually before installing as service:"
echo "    cd $PROJECT_DIR && source venv/bin/activate && python main.py"
echo ""
