#!/usr/bin/env python3
# tools/bangla.py — Bangla Voice Translator, runs as its own process

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pyttsx3
import speech_recognition as sr
from googletrans import Translator
from datetime import datetime


class BanglaVoiceTranslator:
    def __init__(self):
        self.speech = sr.Recognizer()
        self.translator = Translator()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)

    def speak(self, text):
        print(f"[Reply] {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        print("Listening in Bangla...")
        with sr.Microphone() as source:
            self.speech.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = self.speech.listen(source, timeout=5)
                text = self.speech.recognize_google(audio, language="bn")
                print(f"[Bangla] {text}")
                return text
            except (sr.WaitTimeoutError, sr.UnknownValueError, sr.RequestError):
                return None

    def translate(self, bangla_text):
        try:
            result = self.translator.translate(bangla_text, src='bn', dest='en')
            print(f"[Translated] {result.text}")
            return result.text
        except Exception as e:
            print(f"Translation error: {e}")
            return None

    def reply(self, text):
        t = text.lower()
        if any(w in t for w in ['hello', 'hi', 'hey']):
            return "Hello! How can I help you?"
        if 'how are you' in t:
            return "I'm doing great! How about you?"
        if 'your name' in t or 'who are you' in t:
            return "I am a Bangla voice translator."
        if 'time' in t:
            return f"The current time is {datetime.now().strftime('%I:%M %p')}"
        if 'date' in t or 'today' in t:
            return f"Today is {datetime.now().strftime('%B %d, %Y')}"
        if any(w in t for w in ['thank']):
            return "You're welcome!"
        if any(w in t for w in ['bye', 'goodbye', 'quit', 'exit']):
            return "Goodbye! Have a great day!"
        return f"I heard: {text}. I'm still learning!"

    def run(self):
        self.speak("Bangla voice translator is ready. Please speak in Bangla.")
        while True:
            bangla = self.listen()
            if not bangla:
                continue
            english = self.translate(bangla)
            if not english:
                continue
            if any(w in english.lower() for w in ['bye', 'goodbye', 'quit', 'exit']):
                self.speak(self.reply(english))
                break
            self.speak(self.reply(english))
            print("-" * 40)


if __name__ == '__main__':
    BanglaVoiceTranslator().run()
