"""OpenAI-compatible LLM client wrapper."""

from __future__ import annotations

from openai import OpenAI, OpenAIError

from backend.app.core.settings import Settings, get_settings


class LLMClient:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    def complete_json(self, prompt: str) -> str | None:
        if not self.settings.ai_enabled:
            return None

        client = OpenAI(
            api_key=self.settings.openai_api_key,
            base_url=self.settings.openai_base_url,
            timeout=self.settings.openai_timeout_seconds,
        )

        try:
            response = client.chat.completions.create(
                model=self.settings.openai_model,
                messages=[
                    {"role": "system", "content": "You only return valid JSON."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
            )
        except OpenAIError:
            return None

        message = response.choices[0].message.content if response.choices else None
        return message.strip() if message else None
