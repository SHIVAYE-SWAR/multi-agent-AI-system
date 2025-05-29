# llm_utils.py

import requests

def call_llm(prompt, model="gemma:2b"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json()["response"].strip()
    except Exception as e:
        print("Ollama LLM call failed:", e)
        return "Other"
