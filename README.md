# AI Story Shorts Generator

An automated tool to generate viral YouTube Shorts videos using Gemini API, NVIDIA NIM API (Flux.2), Piper TTS, Faster-Whisper, and MoviePy.

## Prerequisites

1. **Python 3.12** installed on your system.
2. **FFmpeg** installed (required for processing video and audio).
3. **ImageMagick** installed (required by MoviePy to render subtitles on Windows).

### Installing FFmpeg (Windows)
1. Download a Windows build from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z) or use a package manager like winget:
   ```cmd
   winget install ffmpeg
   ```
2. If installing manually, extract it to `C:\ffmpeg` and add `C:\ffmpeg\bin` to your System Environment Variables under `Path`.
3. Open a new Command Prompt and run `ffmpeg -version` to verify.

### Installing ImageMagick (Windows)
1. Download the Windows installer from [ImageMagick's official website](https://imagemagick.org/script/download.php#windows).
2. Run the installer. **CRITICAL:** During installation, make sure to check the box: **"Install legacy utilities (e.g. convert)"**.
3. If MoviePy fails to detect ImageMagick automatically, you might need to set the `IMAGEMAGICK_BINARY` environment variable pointing to the `magick.exe` file.
   ```cmd
   set IMAGEMAGICK_BINARY=C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe
   ```

## Installation

1. Open a terminal/command prompt in the application directory.
2. Create a virtual environment (optional but highly recommended):
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install the required Python packages:
   ```cmd
   pip install -r requirements.txt
   ```

## Running the Application

1. Set your Gemini API and NVIDIA API keys as environment variables before running the script. You can get an NVIDIA key for free at build.nvidia.com(Image Generation).
   personal best model is **flux.2-klein-4b**
   
   **On Windows (Command Prompt):**
   ```cmd
   set GEMINI_API_KEY=your_gemini_api_key_here
   set NVIDIA_API_KEY=your_nvidia_api_key_here
   ```
   
   **On Windows (PowerShell):**
   ```powershell
   $env:GEMINI_API_KEY="your_gemini_api_key_here"
   $env:NVIDIA_API_KEY="your_nvidia_api_key_here"
   ```

3. Run the main orchestration script:
   ```cmd
   python main.py
   ```

### Output
The software runs entirely without human interaction. Once completed, check the `output` folder:
- **`output/video/final_video.mp4`**: Your ready-to-upload YouTube Short.
- **`output/thumbnail.jpg`**: A generated thumbnail.
- **`story.txt`** & **`metadata.json`**: Story script, title, and generated hashtags.
