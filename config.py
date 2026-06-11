import os

# Project Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
AUDIO_DIR = os.path.join(OUTPUT_DIR, "audio")
SUBTITLES_DIR = os.path.join(OUTPUT_DIR, "subtitles")
VIDEO_DIR = os.path.join(OUTPUT_DIR, "video")

# File Paths
MUSIC_FILE = os.path.join(ASSETS_DIR, "music.mp3")
FINAL_VIDEO_FILE = os.path.join(VIDEO_DIR, "final_video.mp4")
THUMBNAIL_FILE = os.path.join(OUTPUT_DIR, "thumbnail.jpg")
STORY_TEXT_FILE = os.path.join(BASE_DIR, "story.txt")
METADATA_FILE = os.path.join(BASE_DIR, "metadata.json")
NARRATION_FILE = os.path.join(AUDIO_DIR, "narration.wav")
SUBTITLES_FILE = os.path.join(SUBTITLES_DIR, "subtitles.srt")

# Video Settings
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS = 30
ASPECT_RATIO = "9:16"

# AI Models
GEMINI_MODEL_NAME = "gemini-2.5-flash"
VOICE_NAME = "en-US-ChristopherNeural"
WHISPER_MODEL = "base"

# Audio Mixing
MUSIC_VOLUME = 0.1  # 10% of narration volume
