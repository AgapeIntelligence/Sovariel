import os, httpx
from sovariel_kernel import SOVARIEL

class GrokBridge:
    def __init__(self):
        self.key = os.getenv("XAI_API_KEY") or exit("Set XAI_API_KEY")
        self.client = httpx.Client()

    def ask(self, q):
        try:
            r = self.client.post(
                "https://api.x.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.key}"},
                json={"model":"grok-beta","messages":[{"role":"user","content":q}],"temperature":0.7}
            )
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[offline: {e}]"
