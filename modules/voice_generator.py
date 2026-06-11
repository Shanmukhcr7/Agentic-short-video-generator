import os
import wave
import logging
from pathlib import Path
from config import NARRATION_FILE

def generate_voice(story_data):
    logging.info("Generating highly realistic voice narration with Piper TTS...")
    scenes = story_data.get("scenes", [])
    
    # Combine all narrations into one
    full_text = " ".join([scene.get("narration", "") for scene in scenes])
    
    if not full_text.strip():
        logging.warning("No text found for narration.")
        return story_data
        
    try:
        import piper
        import piper.download_voices
        
        # Save models in a 'models' folder at the root of the project
        model_dir = Path(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models"))
        model_dir.mkdir(parents=True, exist_ok=True)
        
        voice_name = "en_US-ryan-medium"
        model_path = model_dir / f"{voice_name}.onnx"
        
        if not model_path.exists():
            logging.info(f"Downloading high-quality offline voice model ({voice_name}). This only happens once...")
            piper.download_voices.download_voice(voice_name, model_dir)
            
        logging.info("Synthesizing audio...")
        voice = piper.PiperVoice.load(str(model_path))
        
        with wave.open(NARRATION_FILE, "wb") as wav_file:
            voice.synthesize_wav(full_text, wav_file)
            
        logging.info(f"Narration saved successfully to {NARRATION_FILE}")
    except Exception as e:
        logging.error(f"Piper TTS failed: {e}. Falling back to pyttsx3.")
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.save_to_file(full_text, NARRATION_FILE)
            engine.runAndWait()
            logging.info(f"Narration saved with pyttsx3 to {NARRATION_FILE}")
        except Exception as inner_e:
            logging.error(f"Failed to generate narration with pyttsx3: {inner_e}")
            
    return story_data
