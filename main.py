import os
import sys
import logging
from config import *
from modules.utils import setup_logging, create_directories, ensure_assets
from modules.story_generator import generate_story
from modules.image_generator import generate_images
from modules.voice_generator import generate_voice
from modules.subtitle_generator import generate_subtitles
from modules.video_creator import create_video

def main():
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
        
    setup_logging()
    
    print("\n==============================================")
    print("Welcome to AI Story Shorts Generator!")
    print("==============================================")
    while True:
        choice = input("What type of story do you want to generate?\n1: Normal (Cinematic/Viral Content)\n2: Kids (Educational/Pixar Style)\nEnter 1 or 2: ").strip()
        if choice == '1':
            theme = 'normal'
            break
        elif choice == '2':
            theme = 'kids'
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
            
    logging.info(f"Starting AI Story Shorts Generator in '{theme.upper()}' mode...")
    
    # Validate Environment Variables
    if not os.environ.get("GEMINI_API_KEY"):
        logging.error("GEMINI_API_KEY environment variable is missing.")
        logging.error("Please run: set GEMINI_API_KEY=your_api_key")
        sys.exit(1)
        
    create_directories()
    ensure_assets()
    
    try:
        # Step 1: Generate Story (Title, Scenes: Duration, Narration, Image Prompts)
        logging.info("=== STEP 1: Story Generation ===")
        story_data = generate_story(theme)
        
        # Step 2: Generate Images
        logging.info("=== STEP 2: Image Generation ===")
        story_data = generate_images(story_data)
        
        # Step 3: Generate Voiceover
        logging.info("=== STEP 3: Voice Generation ===")
        story_data = generate_voice(story_data)
        
        # Step 4: Generate Subtitles
        logging.info("=== STEP 4: Subtitle Generation ===")
        words_data = generate_subtitles()
        
        # Step 5: Final Video Creation
        logging.info("=== STEP 5: Video Composition ===")
        create_video(story_data, words_data)
        
        logging.info("=== PROCESS COMPLETED SUCCESSFULLY ===")
        logging.info(f"Final video is ready at: {FINAL_VIDEO_FILE}")
        
    except Exception as e:
        logging.exception(f"An error occurred during generation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
