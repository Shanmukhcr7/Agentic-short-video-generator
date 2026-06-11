import os
import json
import logging
import google.generativeai as genai
from config import GEMINI_MODEL_NAME, STORY_TEXT_FILE, METADATA_FILE

def generate_story(theme="normal"):
    logging.info(f"Generating {theme.upper()} story via Gemini API...")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set. Please set it before running.")
    
    genai.configure(api_key=api_key)
    
    if theme == "kids":
        prompt = """
        You are an expert children's story writer.
        Write a 45-60 second story for kids (ages 4-8) that teaches good manners, healthy habits, or an important life lesson.
        Use simple, engaging, and enthusiastic language.
        
        Divide the story into distinct scenes.
        CRITICAL RULE FOR CHARACTER CONSISTENCY: The characters MUST be cute animals (e.g., a bunny, a bear, a kitten) to avoid AI image generation filters. Do NOT use human children. You MUST define a specific, detailed physical description for the main character (e.g. "a fluffy brown bunny wearing a tiny green jacket"). You MUST copy and paste this EXACT SAME physical description into EVERY SINGLE "image_prompt" in the JSON.
        CRITICAL RULE FOR ART STYLE: Every single image_prompt MUST end with the phrase: "3d animation style, pixar style, colorful, cute cartoon, vibrant, masterpiece". Do NOT use the word "kids" or "children" in the image_prompt.
        
        Provide the output EXACTLY as a raw JSON object with no markdown formatting or code blocks.
        """
    else:
        prompt = """
        You are an expert viral YouTube Shorts scriptwriter. 
        Write a 45-60 second story focused on maximizing retention.
        Categories allowed: Emotional, Motivational, Life lessons, Inspirational, Mystery, Suspense, Heartwarming.
        Write in simple English.
        
        Divide the story into distinct scenes.
        CRITICAL RULE FOR CHARACTER CONSISTENCY: You MUST define a specific, detailed physical description for the main character (e.g. "a 25 year old man with messy brown hair wearing a green jacket"). You MUST copy and paste this EXACT SAME physical description into EVERY SINGLE "image_prompt" in the JSON. Do not use generic terms like "a young man" or "he", describe them exactly the same way in every scene so the AI image generator draws the same person.
        
        Provide the output EXACTLY as a raw JSON object with no markdown formatting or code blocks.
        """
    prompt += """
    Format:
    {
      "title": "The Title",
      "description": "Short description for YouTube",
      "hashtags": ["#shorts", "#story", "#motivation"],
      "scenes": [
        {
          "duration": 5,
          "narration": "A young man found a wallet on the road.",
          "image_prompt": "young man finding wallet on street, cinematic, emotional, ultra realistic, 8k"
        }
      ]
    }
    """
    
    # Request JSON response format
    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL_NAME,
        generation_config={"response_mime_type": "application/json"}
    )
    
    response = model.generate_content(prompt)
    
    try:
        story_data = json.loads(response.text)
    except json.JSONDecodeError:
        # Fallback if the model wrapped it in markdown anyway
        text = response.text.replace("```json", "").replace("```", "").strip()
        story_data = json.loads(text)
        
    # Save the text story
    with open(STORY_TEXT_FILE, "w", encoding="utf-8") as f:
        f.write(f"Title: {story_data.get('title', 'Generated Story')}\n\n")
        for i, scene in enumerate(story_data.get('scenes', [])):
            f.write(f"Scene {i+1}: {scene.get('narration', '')}\n")
            
    # Save metadata
    metadata = {
        "title": story_data.get("title", "Generated Story"),
        "description": story_data.get("description", "A generated story."),
        "hashtags": story_data.get("hashtags", ["#shorts", "#story"])
    }
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)
        
    logging.info(f"Story generated successfully. Title: {story_data.get('title')}")
    return story_data
