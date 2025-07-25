# utils/gemini.py

import google.generativeai as genai
import json
import re

# ✅ DIRECTLY SET THE API KEY HERE
api_key = "AIzaSyD7KiMwOYT3o_WDbhKcEgintfUR1ONWwHE"

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-pro")


def enrich_menu_item(title):
    prompt = f"""
    Provide a short (1-2 sentence) description and calorie count for this food or drink item: "{title}".
    Respond in JSON format:
    {{
      "description": "...",
      "calories": "..."
    }}
    """

    try:
        response = model.generate_content(prompt)
        content = response.text

        # Extract JSON using regex
        json_text = re.search(r"\{.*\}", content, re.DOTALL).group()
        return json.loads(json_text)

    except Exception as e:
        print(f"[Gemini Error] For item '{title}':", e)
        return {
            "description": "Description unavailable.",
            "calories": "Unknown"
        }
