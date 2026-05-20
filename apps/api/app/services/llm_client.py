from __future__ import annotations

import httpx

from app.core.config import settings


class LLMClientError(RuntimeError):
    pass


class LLMClient:
    def __init__(self) -> None:
        self.provider = settings.llm_provider.lower()
        self.model = settings.llm_model
        self._api_keys = self._collect_keys()

    def _collect_keys(self) -> list[str]:
        keys: list[str] = []
        if settings.gemini_api_keys:
            keys.extend(k.strip() for k in settings.gemini_api_keys.split(",") if k.strip())
        if settings.gemini_api_key and settings.gemini_api_key not in keys:
            keys.append(settings.gemini_api_key)
        return keys

    def _gemini_generate(self, prompt: str) -> str:
        if not self._api_keys:
            raise LLMClientError("No GEMINI_API_KEY or GEMINI_API_KEYS configured")
        models = [self.model, "gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]
        seen_models: set[str] = set()
        unique_models = []
        for m in models:
            if m not in seen_models:
                seen_models.add(m)
                unique_models.append(m)
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
            for api_key in self._api_keys:
                for model_name in unique_models:
                    url = (
                        f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
                        f"?key={api_key}"
                    )
                    try:
                        response = client.post(url, json=payload)
                        if response.status_code == 429:
                            last_error = f"key …{api_key[-4:]}/{model_name}: quota exhausted"
                            break
                        response.raise_for_status()
                        data = response.json()
                        candidates = data.get("candidates") or []
                        if not candidates:
                            last_error = f"key …{api_key[-4:]}/{model_name}: no candidates"
                            continue
                        parts = candidates[0].get("content", {}).get("parts", [])
                        text = "".join((p.get("text", "") for p in parts if isinstance(p, dict))).strip()
                        if text:
                            return text
                        last_error = f"key …{api_key[-4:]}/{model_name}: empty text"
                    except httpx.HTTPStatusError as exc:
                        if exc.response.status_code == 429:
                            last_error = f"key …{api_key[-4:]}/{model_name}: quota exhausted"
                            break
                        last_error = f"key …{api_key[-4:]}/{model_name}: {exc}"
                        continue
                    except Exception as exc:
                        last_error = f"key …{api_key[-4:]}/{model_name}: {exc}"
                        continue
        raise LLMClientError(f"Gemini generation failed after trying {len(self._api_keys)} key(s): {last_error}")

    def generate(self, prompt: str) -> str:
        if self.provider == "gemini":
            return self._gemini_generate(prompt)
        raise LLMClientError(f"Unsupported LLM provider: {self.provider}")
