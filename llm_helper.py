import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_ollama(prompt: str, model: str = "llama3", system_prompt: str = None) -> str:
    """
    Sends a prompt to the local Ollama LLM instance and returns the response.
    """
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    if system_prompt:
        payload["system"] = system_prompt

    try:
        response = requests.post(OLLAMA_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except requests.exceptions.RequestException as e:
        return f"❌ Error contacting LLM: {e}"