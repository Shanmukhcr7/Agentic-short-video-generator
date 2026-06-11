import logging
from faster_whisper import WhisperModel
from config import NARRATION_FILE, SUBTITLES_FILE, WHISPER_MODEL

def format_timestamp(seconds: float):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def generate_subtitles():
    logging.info("Transcribing audio with faster-whisper to generate subtitles...")
    # Using cpu by default for broad compatibility
    model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
    
    segments, info = model.transcribe(NARRATION_FILE, word_timestamps=True)
    
    words_data = []
    
    with open(SUBTITLES_FILE, "w", encoding="utf-8") as srt_file:
        index = 1
        for segment in segments:
            for word in segment.words:
                start = word.start
                end = word.end
                text = word.word.strip()
                
                # Write to SRT format
                srt_file.write(f"{index}\n")
                srt_file.write(f"{format_timestamp(start)} --> {format_timestamp(end)}\n")
                srt_file.write(f"{text}\n\n")
                index += 1
                
                words_data.append({
                    "word": text,
                    "start": start,
                    "end": end
                })
                
    logging.info(f"Subtitles saved to {SUBTITLES_FILE}")
    return words_data
