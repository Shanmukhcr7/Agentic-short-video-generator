import os
import logging
import urllib.request
from config import *

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def create_directories():
    directories = [OUTPUT_DIR, IMAGES_DIR, AUDIO_DIR, SUBTITLES_DIR, VIDEO_DIR, ASSETS_DIR]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logging.info(f"Ensured directory exists: {directory}")

def ensure_assets():
    """Ensure that the default music.mp3 exists, download a sample if missing."""
    if not os.path.exists(MUSIC_FILE):
        logging.info("Downloading sample background music...")
        try:
            url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
            urllib.request.urlretrieve(url, MUSIC_FILE)
            logging.info("Downloaded sample music.")
        except Exception as e:
            logging.warning(f"Failed to download sample music: {e}. Generating a silent music file as fallback.")
            try:
                from moviepy.editor import AudioClip
                import numpy as np
                make_frame = lambda t: np.zeros((len(t), 2)) if isinstance(t, np.ndarray) else np.zeros(2)
                clip = AudioClip(make_frame, duration=60)
                clip.write_audiofile(MUSIC_FILE, fps=44100, logger=None)
            except Exception as inner_e:
                logging.error(f"Failed to generate silent music: {inner_e}")

def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in " _-").strip()
