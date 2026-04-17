"""DeepSeek API Adapter."""
from .openai import OpenAIAdapter


class DeepSeekAdapter(OpenAIAdapter):
    """Adapter for DeepSeek API (uses OpenAI-compatible format)."""

    BASE_URL = "https://api.deepseek.com/v1/chat/completions"

    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        super().__init__(api_key, model, base_url=self.BASE_URL)
