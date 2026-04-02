# utils/tts.py — TTS helpers
# Child processes import this directly; they get their own engine instance.
# main.py uses the queue-based worker instead (defined at bottom).

import queue
import threading
import pyttsx3


def speak(text: str, voice_index: int = 0, rate: int = 160):
    """Blocking one-shot TTS — use in child processes."""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        if voices and voice_index < len(voices):
            engine.setProperty('voice', voices[voice_index].id)
        engine.setProperty('rate', rate)
        engine.setProperty('volume', 0.9)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"[TTS] {e}")


def speak_female(text: str):
    """Female voice (index 1 on most systems)."""
    speak(text, voice_index=1, rate=140)


def speak_male(text: str):
    """Male voice (index 0 on most systems)."""
    speak(text, voice_index=0, rate=170)


# ── Queue-based worker for main.py ──────────────────────────────────────────

_tts_queue: queue.Queue = queue.Queue()
_engine_lock = threading.Lock()
_engine = None


def _get_engine():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
    return _engine


def tts_worker():
    """Run this in a daemon thread inside main.py only."""
    engine = _get_engine()
    while True:
        try:
            voice_id, text = _tts_queue.get()
            if text is None:
                break
            with _engine_lock:
                voices = engine.getProperty('voices')
                if voices and voice_id < len(voices):
                    engine.setProperty('voice', voices[voice_id].id)
                engine.setProperty('rate', 140 if voice_id == 1 else 170)
                engine.setProperty('volume', 0.9)
                engine.say(text)
                engine.runAndWait()
            _tts_queue.task_done()
        except Exception as e:
            print(f"[TTS worker] {e}")


def talk1(text: str):
    """Female voice — enqueue for main.py worker."""
    _tts_queue.put((1, text))


def talk2(text: str):
    """Male voice — enqueue for main.py worker."""
    _tts_queue.put((0, text))


def wait_for_speech():
    _tts_queue.join()
