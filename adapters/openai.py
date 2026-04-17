"""OpenAI API Adapter."""
import aiohttp
import asyncio
from .base import LLMAdapter


class OpenAIAdapter(LLMAdapter):
    """Adapter for OpenAI API."""

    BASE_URL = "https://api.openai.com/v1/chat/completions"

    def __init__(self, api_key: str, model: str = "gpt-4o-mini", base_url: str = None):
        super().__init__(api_key, model)
        self.base_url = base_url or self.BASE_URL

    def complete(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7) -> str:
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(self.acomplete(prompt, max_tokens, temperature))

    async def acomplete(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7) -> str:
        headers = {
            "authorization": f"Bearer {self.api_key}",
            "content-type": "application/json",
        }
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}],
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url, headers=headers, json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as resp:
                    data = await resp.json()
                    if resp.status != 200:
                        return f"[OpenAI Error {resp.status}]: {data.get('error', {}).get('message', 'Unknown')}"
                    return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[OpenAI Error]: {str(e)}"
