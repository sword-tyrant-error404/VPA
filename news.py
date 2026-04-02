#!/usr/bin/env python3
# media/news.py — News video player, runs as its own process

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import re
import requests
import vlc


def play_news():
    url = 'https://www.nbcnews.com/nightly-news-full-episodes'
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f"SPEAK: Could not fetch news. Error: {e}")
        sys.exit(1)

    links = re.findall(r'https://[^"\s]+\.mp4', res.text)
    if not links:
        print("SPEAK: No news video links found.")
        sys.exit(1)

    video_url = links[0]
    print(f"Playing: {video_url}")
    player = vlc.MediaPlayer(video_url)
    player.play()
    try:
        input("Press Enter to stop...")
    finally:
        player.stop()


if __name__ == '__main__':
    play_news()
