import google.generativeai as genai

model = genai.GenerativeModel("gemini-pro")

def get_gemini_data(item_name):
    prompt = f"""
    Write a menu description for "{item_name}". 
    Estimate calorie count. Then suggest a DALL·E-style image prompt.
    """

    response = model.generate_content(prompt).text

    # crude parsing (we'll improve later)
    lines = response.split("\n")
    description = lines[0].strip()
    calories = next((line for line in lines if "calories" in line.lower()), "N/A")
    image_prompt = lines[-1].strip()

    return {
        "description": description,
        "calories": calories,
        "image_prompt": image_prompt
    }
