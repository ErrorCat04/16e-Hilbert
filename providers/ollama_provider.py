import requests, json, os
from .base import RuleProvider

class OllamaProvider(RuleProvider):
    def __init__(self, model: str = "llama3.1", endpoint: str = "http://localhost:11434/api/generate"):
        self.model = model
        self.endpoint = endpoint
        # charge le system prompt
        here = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(here, "prompts", "system_prompt.txt"), "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

    def solve(self, problem_prompt: str):
        prompt = self._build_prompt(problem_prompt)
        resp = requests.post(self.endpoint, json={
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        text = data.get("response", "").strip()
        # Try to parse JSON
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # fallback: wrap as DSL only
            return {"dsl": text, "evals": [], "final": ""}

    def _build_prompt(self, user_problem: str) -> str:
        return f"{self.system_prompt}\n\nÉNONCÉ UTILISATEUR :\n{user_problem}\n"
