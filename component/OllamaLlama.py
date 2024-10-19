import json
import httpx

OLLAMA_API_BASE = "http://localhost:11434"
DEFAULT_MODEL = "llama3.1:latest"

class OllamaLlama:
    def __init__(self, base_url=OLLAMA_API_BASE):
        self.client = httpx.Client(timeout=60.0)  # Increase timeout to 60 seconds
        self.base_url = base_url

    def chat(self, prompt):
        url = f"{self.base_url}/v1/chat/completions"
        data = {
            "model": "mistral",
            "messages": [{"role": "user", "content": prompt}]
        }
        response = self.client.post(url, json=data, timeout=60.0)  # Specify timeout here as well
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def parse_json_response(self, response):
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return None
