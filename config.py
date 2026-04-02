# config.py — shared constants, no imports from other vpa modules

EMAILS = {
    'shafiq':   '2208018@student.ruet.ac.bd',
    'selim':    '2208015@student.ruet.ac.bd',
    'preta':    '2208036@student.ruet.ac.bd',
    'mohammad': '2208008@student.ruet.ac.bd',
    'apurbo':   '2208027@student.ruet.ac.bd',
}

EMAIL_SENDER = "pythonlusty@gmail.com"

APPS = {
    # Browsers
    "chrome":           {"win": "start chrome",    "linux": "google-chrome", "darwin": "open -a 'Google Chrome'"},
    "google chrome":    {"win": "start chrome",    "linux": "google-chrome", "darwin": "open -a 'Google Chrome'"},
    "firefox":          {"win": "start firefox",   "linux": "firefox",       "darwin": "open -a Firefox"},
    "edge":             {"win": "start msedge",    "linux": "microsoft-edge","darwin": "open -a 'Microsoft Edge'"},
    "brave":            {"win": "start brave",     "linux": "brave-browser", "darwin": "open -a Brave"},
    # Office
    "word":             {"win": "start winword",   "linux": "libreoffice --writer", "darwin": "open -a 'Microsoft Word'"},
    "excel":            {"win": "start excel",     "linux": "libreoffice --calc",   "darwin": "open -a 'Microsoft Excel'"},
    "powerpoint":       {"win": "start powerpnt",  "linux": "libreoffice --impress","darwin": "open -a 'Microsoft PowerPoint'"},
    "notepad":          {"win": "notepad",         "linux": "gedit",         "darwin": "open -a TextEdit"},
    "calculator":       {"win": "calc",            "linux": "gnome-calculator","darwin": "open -a Calculator"},
    "paint":            {"win": "mspaint",         "linux": "gimp",          "darwin": "open -a Preview"},
    # Communication
    "zoom":             {"win": "start zoom",      "linux": "zoom",          "darwin": "open -a zoom.us"},
    "teams":            {"win": "start teams",     "linux": "teams",         "darwin": "open -a 'Microsoft Teams'"},
    "skype":            {"win": "start skype",     "linux": "skype",         "darwin": "open -a Skype"},
    # Media
    "spotify":          {"win": "start spotify",   "linux": "spotify",       "darwin": "open -a Spotify"},
    "vlc":              {"win": "start vlc",       "linux": "vlc",           "darwin": "open -a VLC"},
    # Dev
    "visual studio code": {"win": "code",          "linux": "code",          "darwin": "code"},
    "vscode":           {"win": "code",            "linux": "code",          "darwin": "code"},
    "vs code":          {"win": "code",            "linux": "code",          "darwin": "code"},
    "pycharm":          {"win": "start pycharm64", "linux": "pycharm",       "darwin": "open -a PyCharm"},
    # System
    "task manager":     {"win": "taskmgr",         "linux": "gnome-system-monitor","darwin": "open -a 'Activity Monitor'"},
    "control panel":    {"win": "control",         "linux": "gnome-control-center","darwin": "open -a 'System Preferences'"},
    "file explorer":    {"win": "explorer",        "linux": "nautilus",      "darwin": "open -a Finder"},
    "terminal":         {"win": "cmd",             "linux": "gnome-terminal","darwin": "open -a Terminal"},
    "powershell":       {"win": "powershell",      "linux": "bash",          "darwin": "bash"},
}

WEB_APPS = {
    "claude":       "https://claude.ai",
    "chatgpt":      "https://chat.openai.com",
    "chat gpt":     "https://chat.openai.com",
    "gpt":          "https://chat.openai.com",
    "grok":         "https://x.com/i/grok",
    "gemini":       "https://gemini.google.com",
    "copilot":      "https://copilot.microsoft.com",
    "youtube":      "https://www.youtube.com",
    "facebook":     "https://www.facebook.com",
    "twitter":      "https://twitter.com",
    "x":            "https://x.com",
    "instagram":    "https://www.instagram.com",
    "linkedin":     "https://www.linkedin.com",
    "reddit":       "https://www.reddit.com",
    "telegram":     "https://web.telegram.org/k/",
    "gmail":        "https://mail.google.com",
    "google docs":  "https://docs.google.com",
    "google sheets":"https://sheets.google.com",
    "google drive": "https://drive.google.com",
    "notion":       "https://www.notion.so",
    "trello":       "https://trello.com",
    "git":          "https://github.com",
    "geet":         "https://github.com",
    "stackoverflow":"https://stackoverflow.com",
    "netflix":      "https://www.netflix.com",
    "amazon":       "https://www.amazon.com",
    "daraz":        "https://www.daraz.com.bd/",
}
