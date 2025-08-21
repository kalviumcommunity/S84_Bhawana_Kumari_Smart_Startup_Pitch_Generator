import os 
import requests 
from dotenv import load_dotenv 
# Load environment variables from .env file 
load_dotenv() 
# Get API key from .env 
GROQ_API_KEY = os.getenv("GROQ_API_KEY") 
if not GROQ_API_KEY: raise ValueError("⚠️ GROQ_API_KEY not found. Please add it to your .env file") 
# API endpoint 
url = "https://api.groq.com/openai/v1/chat/completions" 
# Headers 
headers = { "Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json" } 
# Request body (updated model) 
data = { "model": "llama-3.3-70b-versatile", # ✅ supported model 
         "messages": [ 
            {"role": "system", "content": "You are a helpful assistant."}, 
            {"role": "user", "content": "Generate a smart startup pitch idea for an AI-based healthcare app."} ] } 
# Make request 
response = requests.post(url, headers=headers, json=data) 
# Print result 
if response.status_code == 200:
    result = response.json() 
    print(result["choices"][0]["message"]["content"]) 
else:
    print("Error:", response.status_code, response.text)