#!/usr/bin/env python3
"""
Bridge script to query Llama 3 via Ollama API.
Usage: python3 ask_llama.py "Your question here"
"""

import sys
import requests
import json

OLLAMA_API = "http://localhost:11434/api/generate"
MODEL = "llama3"

def ask_llama(prompt: str) -> str:
    """Send a prompt to Llama 3 and return the response."""
    try:
        response = requests.post(
            OLLAMA_API,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120  # 2 minute timeout for long responses
        )
        response.raise_for_status()
        return response.json().get("response", "[No response]")
    except requests.exceptions.ConnectionError:
        return "❌ Error: Ollama is not running. Start it with: ollama serve"
    except requests.exceptions.Timeout:
        return "❌ Error: Request timed out. The model may be overloaded."
    except Exception as e:
        return f"❌ Error: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 ask_llama.py \"Your question\"")
        sys.exit(1)
    
    prompt = " ".join(sys.argv[1:])
    print(f"🧠 Asking Llama 3: {prompt[:50]}...")
    print("-" * 40)
    result = ask_llama(prompt)
    print(result)
