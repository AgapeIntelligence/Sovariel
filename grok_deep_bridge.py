import os
import asyncio
import httpx
from sovariel_kernel import SOVARIEL

XAI_API_KEY = os.getenv("XAI_API_KEY")
if not XAI_API_KEY:
    raise RuntimeError("Set XAI_API_KEY")

SOVARIEL.register_agent("Grok", "ai")

async def grok_think(prompt: str):
    async with httpx.AsyncClient() as client:
        r = await client.post(
            "https://api.x.ai/v1/chat/completions",
            headers={"Authorization": f"Bearer {XAI_API_KEY}"},
            json={
                "messages": [{"role": "user", "content": prompt}],
                "model": "grok-beta",
                "temperature": 0.3
            }
        )
        reply = r.json()["choices"][0]["message"]["content"]
        boost = len(reply.split()) * 0.0005
        SOVARIEL.agents["Grok"]['agape_gate'] = min(1.0, SOVARIEL.agents["Grok"]['agape_gate'] + boost)
        SOVARIEL.trigger_hook("coherence_update")
        return reply

async def main():
    print("Grok triad bridge active")
    while True:
        try:
            msg = input("You → ")
            if msg.lower() in ["quit","exit"]]: break
            reply = await grok_think(msg)
            print(f"Grok → {reply}")
            print(f"Coherence: {SOVARIEL.galactic_coherence():.4f}")
        except: break

if __name__ == "__main__":
    asyncio.run(main())
