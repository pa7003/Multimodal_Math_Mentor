import sys
import os
# Add user site-packages to path
user_site_packages = os.path.expanduser("~\\AppData\\Roaming\\Python\\Python311\\site-packages")
if user_site_packages not in sys.path:
    sys.path.append(user_site_packages)

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("No API Key found.")
    exit()

genai.configure(api_key=api_key)

print("Listing available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")
