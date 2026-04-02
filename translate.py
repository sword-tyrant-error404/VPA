#!/usr/bin/env python3
# tools/translate.py — Turtle Dictionary Translator, runs as its own process

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import turtle as t
from io import BytesIO
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from googletrans import Translator

LANG_CODES = {
    "english": "en", "chinese": "zh", "spanish": "es",
    "french": "fr",  "japanese": "ja", "portuguese": "pt",
    "russian": "ru", "korean": "ko",  "german": "de",
    "italian": "it", "bangla": "bn",
}


class TurtleTranslator:
    def __init__(self):
        self.screen = t.Screen()
        self.screen.setup(800, 600)
        self.screen.bgcolor('light blue')
        self.screen.title("Dictionary Translator")
        self.writer = t.Turtle()
        self.writer.hideturtle(); self.writer.up(); self.writer.speed(0)
        self.translator = Translator()
        self._draw_interface()

    def _draw_interface(self):
        self.writer.clear()
        self.writer.goto(0, 250)
        self.writer.write("Dictionary Translator", align="center", font=("Arial", 24, "bold"))
        self.writer.goto(0, 200)
        self.writer.write("Enter English text to translate", align="center", font=("Arial", 14, "normal"))
        self.writer.goto(0, 150)
        self.writer.write(", ".join(LANG_CODES.keys()), align="center", font=("Arial", 11, "normal"))
        t.update()

    def _tts(self, text, lang_code):
        try:
            tts = gTTS(text=text, lang=lang_code)
            buf = BytesIO(); tts.write_to_fp(buf); buf.seek(0)
            play(AudioSegment.from_mp3(buf))
        except Exception as e:
            print(f"Audio error: {e}")

    def run(self):
        while True:
            text = t.textinput("Input", "Enter English text (or 'quit'):")
            if not text or text.lower() == 'quit':
                break
            lang = t.textinput("Language", "Target language:")
            if not lang or lang.lower() == 'quit':
                break
            lang = lang.lower().strip()
            if lang not in LANG_CODES:
                self._draw_interface()
                self.writer.goto(0, 50)
                self.writer.write("Invalid language!", align="center", font=("Arial", 14, "normal"))
                continue
            self._draw_interface()
            self.writer.goto(0, 50)
            self.writer.write(f"English: {text}", align="center", font=("Arial", 14, "normal"))
            try:
                result = self.translator.translate(text, dest=LANG_CODES[lang])
                translated = result.text
            except Exception as e:
                translated = f"Error: {e}"
            self.writer.goto(0, 0); self.writer.color("blue")
            self.writer.write(f"{lang.title()}: {translated}", align="center", font=("Arial", 16, "bold"))
            self.writer.color("black"); t.update()
            self._tts(translated, LANG_CODES[lang])
        t.bye()


if __name__ == '__main__':
    TurtleTranslator().run()
