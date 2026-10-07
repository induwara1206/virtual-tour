from google import genai
import json
import os

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("GEMINI_API_KEY is not set. See README 5.5.")

client = genai.Client(api_key=api_key)

PLACES = {
    "colombo": "Colombo Port City, Sri Lanka",
    "galle-fort": "Galle Fort, Sri Lanka",
    "sigiriya": "Sigiriya Rock Fortress, Sri Lanka",
    "ella": "Ella, Sri Lanka",
    "kandy-lake": "Kandy Lake, Sri Lanka",
}


def generate_info(place_name):
    prompt = f"""Write short tourism information about {place_name}.
Respond ONLY with valid JSON in this exact format, no other text, no markdown formatting:
{{
  "about": "2-3 sentences about what this place is",
  "history": "2-3 sentences about its history or culture",
  "weather": "1-2 sentences about typical weather/climate there",
  "tips": "1-2 sentences of practical visitor tips"
}}"""

    response = client.models.generate_content(
               model="gemini-3.5-flash-lite",
        contents=prompt
    )
    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return text.strip()


results = {}
for slug, place_name in PLACES.items():
    print(f"Generating content for {place_name}...")
    text = generate_info(place_name)
    try:
        results[slug] = json.loads(text)
    except json.JSONDecodeError:
        print(f"Could not parse response for {place_name}, raw text saved instead.")
        results[slug] = {"raw": text}

with open("destination_content.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\nDone! Saved to destination_content.json")