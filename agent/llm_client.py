import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ==========================================
# G R O Q   C O N F I G U R A T I O N
# (Commented out - Swap back if needed)
# ==========================================
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# MODEL_NAME = "llama-3.3-70b-versatile"
# URL = "https://api.groq.com/openai/v1/chat/completions"
# HEADERS = {
#     "Authorization": f"Bearer {GROQ_API_KEY}",
#     "Content-Type": "application/json"
# }

# ==========================================
# L O C A L   O L L A M A   C O N F I G
# (Using OpenAI compatible endpoint for stability)
# ==========================================
MODEL_NAME = "qwen2.5-coder:7b-instruct-q4_K_M"
URL = "http://localhost:11434/v1/chat/completions" 
HEADERS = {"Content-Type": "application/json"}

def call_llm(messages):
    
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0
    }

    try:
        response = requests.post(
            URL,
            headers=HEADERS,
            json=payload
        )
        
        # Check for HTTP errors
        if response.status_code != 200:
            print(f"\n[ERROR] Ollama returned {response.status_code}: {response.text}")
            response.raise_for_status()

        data = response.json()

        # Handle OpenAI / Ollama V1 response format
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
            
        raise KeyError(f"Unexpected API response format: {data}")
        
    except requests.exceptions.RequestException as e:
        print(f"\n[ERROR] LLM Request failed: {e}")
        # If the specific tag fails, let's suggest checking 'ollama list'
        print(f"TIP: Verify your model name. Run 'ollama list' and ensure it matches '{MODEL_NAME}'.")
        raise