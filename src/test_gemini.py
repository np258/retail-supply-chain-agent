import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

print("Fetching available models for your API key...\n")

try:
    models = list(client.models.list())
    for m in models:
        # Print models that support content generation
        if "generateContent" in getattr(m, "supported_generation_methods", []):
            print(f"- {m.name}")
except Exception as e:
    print("Failed to fetch models:")
    print(e)