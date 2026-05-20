from __future__ import annotations

import httpx

from app.core.config import settings


class LLMClientError(RuntimeError):
    pass


class LLMClient:
    def __init__(self) -> None:
        self.provider = settings.llm_provider.lower()
        self.model = settings.llm_model
        self.gemini_api_key = settings.gemini_api_key

    def _gemini_generate(self, prompt: str) -> str:
        if not self.gemini_api_key:
            raise LLMClientError("GEMINI_API_KEY is not configured")
        models = [self.model, "gemini-1.5-flash-latest", "gemini-1.5-pro-latest", "gemini-1.0-pro"]
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.2,
                "topK": 20,
                "topP": 0.9,
                "maxOutputTokens": 1024,
            },
        }
        last_error = "unknown"
        with httpx.Client(timeout=40.0) as client:
            for model_name in models:
                url = (
                    f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
                    f"?key={self.gemini_api_key}"
                )
                try:
                    response = client.post(url, json=payload)
                    response.raise_for_status()
                    data = response.json()
                    candidates = data.get("candidates") or []
                    if not candidates:
                        last_error = f"{model_name}: no candidates"
                        continue
                    parts = candidates[0].get("content", {}).get("parts", [])
                    text = "".join((p.get("text", "") for p in parts if isinstance(p, dict))).strip()
                    if text:
                        return text
                    last_error = f"{model_name}: empty text"
                except Exception as exc:
                    last_error = f"{model_name}: {exc}"
                    continue
        raise LLMClientError(f"Gemini generation failed: {last_error}")

    def generate(self, prompt: str) -> str:
        if self.provider == "gemini":
            return self._gemini_generate(prompt)
        raise LLMClientError(f"Unsupported LLM provider: {self.provider}")
