#!/usr/bin/env python3
# tools/email_tool.py — runs as its own process

import sys
import os
import smtplib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import EMAILS, EMAIL_SENDER
from utils.tts import speak_female as talk1, speak_male as talk2

try:
    import pyautogui
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False

try:
    import speech_recognition as sr
    HAS_SR = True
except ImportError:
    HAS_SR = False


def listen_once() -> str:
    if not HAS_SR:
        return input(">>> ").lower().strip()
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source, timeout=5)
            return r.recognize_google(audio).lower().strip()
    except Exception:
        return input(">>> ").lower().strip()


def get_recipient():
    talk1("Whom do you want to send the mail?")
    emails = dict(EMAILS)  # local mutable copy

    while True:
        name = listen_once()
        if name in emails:
            return name, emails[name]
        talk2("I don't recognise that name.")
        name = input("Type the name: ").lower().strip()
        if name in emails:
            return name, emails[name]
        addr = input("Enter roll number or full email: ").strip()
        if '@' in addr:
            email_addr = addr
        else:
            email_addr = f"{addr}@student.ruet.ac.bd"
        emails[name] = email_addr
        return name, email_addr


def get_body_speech():
    talk1("Speak your subject.")
    subject = listen_once()
    talk1("Speak your message body.")
    body = listen_once()
    return subject, body


def get_body_typed():
    subject = input("Subject: ").strip()
    body = input("Body: ").strip()
    return subject, body


def review_and_confirm(receiver, email_addr, subject, body) -> bool:
    print(f"\n--- Email Review ---\nTo: {receiver} <{email_addr}>\nSubject: {subject}\nBody:\n{body}\n---")
    if HAS_PYAUTOGUI:
        try:
            pyautogui.alert(
                f"To: {receiver}\nEmail: {email_addr}\nSubject: {subject}\nBody:\n{body}",
                title="Email Review"
            )
        except Exception:
            pass
    ans = input("Send? (yes/no): ").lower().strip()
    return ans == 'yes'


def send_email(sender, password, recipient_email, subject, body):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, recipient_email, f"Subject: {subject}\n\n{body}")
    server.quit()


def main():
    receiver, recipient_email = get_recipient()
    talk1(f"Sending mail to {receiver}.")

    talk2("Say 1 for speech input, say 2 for typed input.")
    mode = input("Mode (1=speech / 2=type): ").strip()
    if mode == '1':
        subject, body = get_body_speech()
    else:
        subject, body = get_body_typed()

    if not review_and_confirm(receiver, recipient_email, subject, body):
        talk2("Email cancelled.")
        return

    password = os.getenv("EMAIL_PASSWORD", "ypsazczivgabqsyd")
    try:
        send_email(EMAIL_SENDER, password, recipient_email, subject, body)
        talk1("Email sent successfully!")
        print("Email sent.")
    except Exception as e:
        talk2(f"Failed to send email. Error: {e}")
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
