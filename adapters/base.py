"""Base LLM Adapter Interface."""
from abc import ABC, abstractmethod


class LLMAdapter(ABC):
    """Abstract base class for LLM adapters."""

    def __init__(self, api_key: str, model: str = "default"):
        self.api_key = api_key
        self.model = model

    @abstractmethod
    def complete(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7) -> str:
        """Synchronous completion."""
        pass

    @abstractmethod
    async def acomplete(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7) -> str:
        """Asynchronous completion."""
        pass

    def estimate_tokens(self, text: str) -> int:
        """Rough token estimation."""
        return len(text) // 4
