import os
import io
import base64
import logging
import requests
from PIL import Image, ImageDraw

from config import IMAGES_DIR

def generate_images(story_data):
    logging.info("Generating images for scenes using NVIDIA NIM API...")
    scenes = story_data.get("scenes", [])
    
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        logging.error("NVIDIA_API_KEY environment variable is missing!")
        logging.error("Please get a free API key from build.nvidia.com and run: set NVIDIA_API_KEY=your_key")
        for i, scene in enumerate(scenes):
            image_path = os.path.join(IMAGES_DIR, f"scene_{i+1:02d}.png")
            _generate_placeholder(scene, image_path, i+1)
        return story_data

    for i, scene in enumerate(scenes):
        image_path = os.path.join(IMAGES_DIR, f"scene_{i+1:02d}.png")
        prompt = scene.get("image_prompt", "") + ", cinematic movie scene, high quality, highly detailed, 8k"
        
        logging.info(f"Generating image for Scene {i+1} using NVIDIA Flux.2 Klein 4B...")
        success = False
        
        try:
            url = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.2-klein-4b"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            payload = {
                "prompt": prompt,
                "width": 1024,
                "height": 1024,
                "seed": 0,
                "steps": 4
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            if response.status_code == 200:
                data = response.json()
                artifacts = data.get("artifacts", [{}])
                b64_image = artifacts[0].get("base64")
                if b64_image:
                    img_data = base64.b64decode(b64_image)
                    img = Image.open(io.BytesIO(img_data))
                    
                    # Center crop to 9:16 aspect ratio (1080:1920)
                    target_ratio = 1080 / 1920
                    img_ratio = img.width / img.height
                    
                    if img_ratio > target_ratio:
                        new_width = int(target_ratio * img.height)
                        offset = (img.width - new_width) // 2
                        img = img.crop((offset, 0, offset + new_width, img.height))
                    else:
                        new_height = int(img.width / target_ratio)
                        offset = (img.height - new_height) // 2
                        img = img.crop((0, offset, img.width, offset + new_height))
                        
                    img = img.resize((1080, 1920), Image.LANCZOS)
                    img.save(image_path)
                    scene["image_path"] = image_path
                    logging.info(f"Successfully generated AI image for Scene {i+1}")
                    success = True
                else:
                    logging.warning(f"NVIDIA API returned 200 but no base64 image. Response: {data}")
            else:
                logging.error(f"NVIDIA API Error: {response.status_code} - {response.text}")
        except Exception as e:
            logging.warning(f"NVIDIA API Request Failed for scene {i+1}: {e}")
        
        if not success:
            _generate_placeholder(scene, image_path, i+1)
            
    return story_data

def _generate_placeholder(scene, image_path, scene_num):
    logging.warning(f"Generating a placeholder image for scene {scene_num} instead.")
    import random
    color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
    img = Image.new('RGB', (1080, 1920), color=color)
    d = ImageDraw.Draw(img)
    d.text((100, 960), f"Scene {scene_num} Placeholder", fill=(255, 255, 255))
    img.save(image_path)
    scene["image_path"] = image_path
