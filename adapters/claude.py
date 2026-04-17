"""Claude API Adapter."""
import aiohttp
import asyncio
from .base import LLMAdapter


class ClaudeAdapter(LLMAdapter):
    """Adapter for Anthropic Claude API."""

    BASE_URL = "https://api.anthropic.com/v1/messages"

    def __init__(self, api_key: str, model: str = "claude-3-5-haiku-20241022"):
        super().__init__(api_key, model)

    def complete(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7) -> str:
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(self.acomplete(prompt, max_tokens, temperature))

    async def acomplete(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7) -> str:
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
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
                    self.BASE_URL, headers=headers, json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as resp:
                    data = await resp.json()
                    if resp.status != 200:
                        return f"[Claude Error {resp.status}]: {data.get('error', {}).get('message', 'Unknown')}"
                    return data["content"][0]["text"]
        except Exception as e:
            return f"[Claude Error]: {str(e)}"
