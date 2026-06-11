import os
import logging
import numpy as np
from PIL import Image
from moviepy.editor import (
    VideoFileClip, AudioFileClip, ImageClip, TextClip, 
    CompositeVideoClip, CompositeAudioClip, concatenate_videoclips,
    afx
)
from config import (
    IMAGES_DIR, MUSIC_FILE, NARRATION_FILE, FINAL_VIDEO_FILE, THUMBNAIL_FILE,
    VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS, MUSIC_VOLUME
)

def zoom_in_effect(clip, zoom_ratio=0.04):
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size

        new_size = [
            int(img.size[0] * (1 + (zoom_ratio * t / clip.duration))),
            int(img.size[1] * (1 + (zoom_ratio * t / clip.duration)))
        ]
        
        img = img.resize(new_size, Image.BILINEAR)
        
        x = int((new_size[0] - base_size[0]) / 2)
        y = int((new_size[1] - base_size[1]) / 2)
        
        img = img.crop((x, y, x + base_size[0], y + base_size[1]))
        return np.array(img)

    return clip.fl(effect)

def create_subtitle_clip(text, start, duration, width, height):
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np
    from moviepy.editor import ImageClip
    
    # We need a dummy image just to get the bbox with the font
    dummy_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
    d_dummy = ImageDraw.Draw(dummy_img)
    try:
        font = ImageFont.truetype("arialbd.ttf", 90)
    except:
        font = ImageFont.load_default()
        
    bbox = d_dummy.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    stroke_width = 4
    padding = stroke_width + 10
    
    img_w = int(text_width + padding * 2)
    img_h = int(text_height + padding * 2)
    
    img = Image.new('RGBA', (img_w, img_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    
    # Draw text at origin with padding
    text_x = padding - bbox[0]
    text_y = padding - bbox[1]
    
    # Draw stroke
    for offset_x in range(-stroke_width, stroke_width + 1):
        for offset_y in range(-stroke_width, stroke_width + 1):
            if offset_x != 0 or offset_y != 0:
                d.text((text_x + offset_x, text_y + offset_y), text, font=font, fill="black")
                
    # Draw text
    d.text((text_x, text_y), text, font=font, fill="yellow")
    
    clip = ImageClip(np.array(img)).set_start(start).set_duration(duration)
    alpha = np.array(img)[:, :, 3] / 255.0
    from moviepy.video.VideoClip import ImageClip as MaskClip
    mask = MaskClip(alpha, ismask=True).set_start(start).set_duration(duration)
    clip = clip.set_mask(mask)
    
    # Position the small clip on the video
    x_pos = (width - img_w) / 2
    y_pos = height - 400
    clip = clip.set_position((x_pos, y_pos))
        
    return clip

def create_video(story_data, words_data):
    logging.info("Starting video creation and composition...")
    
    scenes = story_data.get("scenes", [])
    if not scenes:
        raise ValueError("No scenes found to create video.")
        
    narration_audio = AudioFileClip(NARRATION_FILE)
    # Add 1.0 second padding to avoid audio/video cutting at the very end
    total_duration = narration_audio.duration + 1.0
    
    overlap = 0.5
    scene_duration = (total_duration + (len(scenes) - 1) * overlap) / len(scenes)
    
    video_clips = []
    current_start = 0.0
    
    for i, scene in enumerate(scenes):
        img_path = scene.get("image_path")
        if not img_path or not os.path.exists(img_path):
            img_path = os.path.join(IMAGES_DIR, f"scene_{i+1:02d}.png")
            
        clip = ImageClip(img_path).set_duration(scene_duration)
        clip = clip.resize(newsize=(VIDEO_WIDTH, VIDEO_HEIGHT))
        
        # Apply Ken Burns zoom effect
        clip = zoom_in_effect(clip, zoom_ratio=0.05)
        
        clip = clip.set_start(current_start)
        
        # Crossfade transition (fade in for subsequent clips)
        if i > 0:
            clip = clip.crossfadein(overlap)
            
        video_clips.append(clip)
        current_start += scene_duration - overlap
        
    # Save a thumbnail frame from the first clip
    if video_clips:
        logging.info("Saving thumbnail image...")
        video_clips[0].save_frame(THUMBNAIL_FILE, t=0.5)
        
    # Combine scene clips with proper overlapping crossfades
    final_video = CompositeVideoClip(video_clips, size=(VIDEO_WIDTH, VIDEO_HEIGHT))
    
    # Subtitles overlay
    subtitle_clips = []
    for word_info in words_data:
        word = word_info["word"]
        start = word_info["start"]
        end = word_info["end"]
        duration = end - start
        
        try:
            txt_clip = create_subtitle_clip(word, start, duration, VIDEO_WIDTH, VIDEO_HEIGHT)
            subtitle_clips.append(txt_clip)
        except Exception as e:
            logging.error(f"Failed to create subtitle clip: {e}")
            break

    if subtitle_clips:
        final_video = CompositeVideoClip([final_video] + subtitle_clips)
        
    # Audio background music
    bg_music = AudioFileClip(MUSIC_FILE).fx(afx.volumex, MUSIC_VOLUME)
    if bg_music.duration < total_duration:
        bg_music = afx.audio_loop(bg_music, duration=total_duration)
    else:
        bg_music = bg_music.subclip(0, total_duration)
        
    final_audio = CompositeAudioClip([narration_audio, bg_music])
    
    final_video = final_video.set_audio(final_audio)
    final_video = final_video.set_duration(total_duration)
    
    logging.info("Rendering final video. This may take a while...")
    final_video.write_videofile(
        FINAL_VIDEO_FILE,
        fps=VIDEO_FPS,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="ultrafast",
        remove_temp=False
    )
    
    logging.info(f"Video creation completed: {FINAL_VIDEO_FILE}")
