import os, requests, json
from .base import RuleProvider

class OpenRouterProvider(RuleProvider):
    def __init__(self, model: str = "meta-llama/llama-3.1-8b-instruct:free",
                 endpoint: str = "https://openrouter.ai/api/v1/chat/completions"):
        self.model = model
        self.endpoint = endpoint
        here = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(here, "prompts", "system_prompt.txt"), "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

    def solve(self, problem_prompt: str):
        api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
        if not api_key:
            # Pas de clé : fallback minimal
            return {"dsl": "DEFINE ⊕ WITH max(a,b)", "evals": ["3 ⊕ 7"], "final": "Aucune clé API fournie, fallback."}

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": problem_prompt}
            ],
            "temperature": 0.2,
        }
        r = requests.post(self.endpoint, headers=headers, json=body, timeout=120)
        r.raise_for_status()
        data = r.json()
        text = data["choices"][0]["message"]["content"].strip()
        try:
            return json.loads(text)
        except Exception:
            return {"dsl": text, "evals": [], "final": ""}
