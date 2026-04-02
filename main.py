#!/usr/bin/env python3
"""
VPA (Virtual Personal Assistant) - Main Entry Point
Clean modular implementation using subprocess architecture.
"""

import sys
import time
import threading
import speech_recognition as sr
import pyjokes
import pyautogui
import webbrowser
import subprocess
import wikipedia
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Import configuration
from config import WEB_APPS

# Import launcher utilities
from utils.launcher import launch, launch_and_listen

# Import TTS utilities
from utils.tts import talk1, talk2, tts_worker

# Import platform utilities
from utils.platform import open_app, open_camera, kill_camera, take_screenshot


def take_command() -> str:
    """Listen for voice command via microphone."""
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            command = r.recognize_google(audio).lower()
            print(f"Recognized: {command}")

            # Wake word detection
            if 'alexa' in command:
                command = command.replace('alexa', '').strip()
                return command
            return ''
    except sr.UnknownValueError:
        return ''
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
        return ''
    except Exception as e:
        print(f"Microphone error: {e}")
        return ''


def show_instructions():
    """Display available commands."""
    instructions = """VPA Commands:
- Say "play <song>" to play YouTube music
- Say "time" or "date" for current time/date
- Say "timer for X hours/minutes" to set a timer
- Say "alarm for 7 a.m." to set an alarm
- Say "send email" to send an email
- Say "joke" to hear a joke
- Say "news" to watch news video
- Say "show me" to take a selfie
- Say "draw me" to draw a screenshot
- Say "screenshot" to capture screen
- Say "google <query>" to search Google
- Say "open <app>" to launch applications
- Say "dictionary" for translation tool
- Say "bangla" for Bangla voice translator
- Say "tik tak toe" to play Tic-Tac-Toe
- Say "connect computer" for Connect Four (vs AI)
- Say "connect" for Connect Four (2-player)
- Say "word game" for Guess The Word
- Say "market for <company>" for stock prices
- Say "price of <crypto>" for cryptocurrency prices
- Say "instruction" to see this help
- Say "stop" to exit
"""
    print(instructions)
    return instructions


def process_command(command: str) -> bool:
    """
    Process a voice command.
    Returns False if the assistant should exit, True otherwise.
    """
    # Exit command
    if 'stop' in command and 'alexa' not in command:
        talk2("Goodbye!")
        return False

    # Help command
    if 'instruction' in command:
        threading.Thread(target=lambda: print(show_instructions()), daemon=True).start()
        return True

    # Time
    if 'time' in command and 'timer' not in command:
        current_time = time.strftime('%I:%M %p')
        talk1(f"The current time is {current_time}")
        return True

    # Date
    if 'date' in command:
        current_date = time.strftime('%B %d, %Y')
        talk1(f"Today's date is {current_date}")
        return True

    # Play YouTube
    if 'play' in command:
        query = command.replace('play', '').strip()
        import pywhatkit
        talk1(f"Playing {query} on YouTube")
        pywhatkit.playonyt(query)
        return True

    # Google search
    if 'google' in command:
        query = command.replace('google', '').strip()
        import webbrowser
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        talk1(f"Searching Google for {query}")
        return True

    # Screenshot
    if 'screenshot' in command or 'take screenshot' in command:
        talk1("Taking screenshot")
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        try:
            import pyautogui
            pyautogui.screenshot(filename)
            talk1(f"Screenshot saved as {filename}")
        except Exception as e:
            talk2(f"Screenshot failed: {e}")
        return True

    # Timer
    if 'timer for' in command and ('hour' in command or 'minute' in command):
        talk1("Setting timer")
        launch_and_listen('tools/timer.py', command, speak_cb=talk1)
        return True

    # Alarm
    if 'alarm for' in command and ('a.m.' in command or 'p.m.' in command):
        talk1("Setting alarm")
        launch_and_listen('tools/alarm.py', command, speak_cb=talk1)
        return True

    # Send email
    if 'send' in command and 'email' in command:
        talk1("Opening email tool")
        launch('tools/email_tool.py')
        return True

    # Joke
    if 'joke' in command:
        import pyjokes
        joke = pyjokes.get_joke()
        talk1(joke)
        return True

    # News
    if 'news' in command:
        talk1("Opening news")
        launch('media/news.py')
        return True

    # Take photo
    if 'show me' in command:
        talk1("Taking photo")
        open_camera()
        time.sleep(2)
        screenshot_file = take_screenshot("selfie.png")
        kill_camera()
        if screenshot_file:
            talk1("Photo captured")
        return True

    # Draw screenshot
    if 'draw me' in command:
        talk1("Starting drawing")
        launch('media/draw.py')
        return True

    # Bangla translator
    if 'bangla' in command:
        talk1("Starting Bangla voice translator")
        launch('tools/bangla.py')
        return True

    # Dictionary translator
    if 'dictionary' in command:
        talk1("Opening dictionary translator")
        launch('tools/translate.py')
        return True

    # Games
    if 'tik' in command and ('tak' in command or 'toe' in command):
        talk1("Starting Tic Tac Toe")
        launch('games/tiktaktoe.py')
        return True

    if 'connect' in command and 'computer' in command:
        talk1("Starting Connect Four against computer")
        launch('games/connect4_ai.py')
        return True

    if 'connect' in command:
        talk1("Starting Connect Four for two players")
        launch('games/connect4_2p.py')
        return True

    if 'word' in command and 'game' in command:
        talk1("Starting Guess The Word game")
        launch('games/wordgame.py')
        return True

    # Stock prices
    if 'market for' in command:
        company = command.split('market for')[1].strip()
        talk1(f"Looking up stock for {company}")
        launch('media/stock.py', *company.split())
        return True

    # Cryptocurrency prices
    if 'price of' in command:
        crypto = command.split('price of')[1].strip().lower()
        talk1(f"Tracking {crypto} price")
        launch('media/crypto.py', crypto)
        return True

    # Open desktop application or web app
    if 'open' in command:
        app_name = command.replace('open', '').strip().lower()

        # Try desktop app first using platform helper
        if open_app(app_name):
            talk1(f"Opening {app_name}")
            return True

        # Try web app
        if app_name in WEB_APPS:
            talk1(f"Opening {app_name} in browser")
            try:
                webbrowser.open(WEB_APPS[app_name])
            except Exception as e:
                talk2(f"Failed to open {app_name}: {e}")
            return True

        talk2(f"I don't know how to open {app_name}")
        return True

    # Joke
    if 'joke' in command:
        try:
            joke = pyjokes.get_joke()
            talk1(joke)
        except Exception as e:
            talk2(f"Couldn't get a joke: {e}")
        return True

    # Press a key
    if 'press' in command and 'press' == command.split()[0]:
        key = command.replace('press', '').strip()
        if key:
            pyautogui.press(key)
            talk1(f"Pressed {key}")
        return True

    # Type text
    if 'type' in command and 'type' == command.split()[0]:
        text = command.replace('type', '').strip()
        if text:
            pyautogui.write(text, interval=0.08)
            talk1(f"Typed {text}")
        return True

    # Keyboard shortcut (hotkey)
    if 'map' in command:
        keys = command.replace('map', '').strip().split()
        if len(keys) >= 2:
            pyautogui.hotkey(*keys)
            talk1(f"Pressed shortcut {'+'.join(keys)}")
        return True

    # Cancel/close window
    if 'cancel' in command or 'stop program' in command:
        pyautogui.hotkey('alt', 'f4')
        talk1("Closing program")
        return True

    # Download YouTube video
    if 'download' in command:
        talk2("Enter link of the video or audio")
        link = input("Enter YouTube URL: ").strip()
        if link:
            try:
                talk2("Downloading, please wait...")
                result = subprocess.run(['yt-dlp', link], capture_output=True, text=True)
                if result.returncode == 0:
                    talk2("Download completed")
                else:
                    talk2("Download failed")
            except FileNotFoundError:
                talk2("yt-dlp is not installed")
            except Exception as e:
                talk2(f"Download error: {e}")
        return True

    # General knowledge query (Wikipedia)
    if len(command) > 6:
        try:
            talk1(f"Searching for {command}")
            # Filter out any special characters that might cause issues
            query = command.strip()
            summary = wikipedia.summary(query, sentences=3)
            talk2(summary)
        except wikipedia.DisambiguationError as e:
            talk1("The query is too ambiguous. Please be more specific.")
        except wikipedia.PageError:
            talk1("I couldn't find any information on that topic.")
        except Exception as e:
            talk2(f"Search error: {e}")
        return True

    return True


def main():
    """Main VPA loop."""
    # Start TTS worker thread
    tts_thread = threading.Thread(target=tts_worker, daemon=True)
    tts_thread.start()

    # Wait for TTS engine to initialize
    time.sleep(1)

    # Greet user
    talk2("Hello! I'm your Virtual Personal Assistant. How can I help you?")

    # Show instructions
    instructions = show_instructions()
    talk1("Say 'alexa' followed by your command.")

    # Main loop
    try:
        while True:
            command = take_command()
            if command:
                should_continue = process_command(command)
                if not should_continue:
                    break
            time.sleep(0.5)
    except KeyboardInterrupt:
        talk2("Goodbye!")
    except Exception as e:
        print(f"Error: {e}")
        talk2("An error occurred. Shutting down.")


if __name__ == '__main__':
    main()
