from __future__ import annotations

import logging

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMClientError(RuntimeError):
    pass


class LLMClient:
    def __init__(self) -> None:
        self.provider = settings.llm_provider.lower()
        self.model = settings.llm_model
        self._api_keys = self._collect_keys()

    def _collect_keys(self) -> list[str]:
        seen: set[str] = set()
        keys: list[str] = []
        if settings.gemini_api_keys:
            for k in settings.gemini_api_keys.split(","):
                k = k.strip()
                if k and k not in seen:
                    seen.add(k)
                    keys.append(k)
        if settings.gemini_api_key:
            k = settings.gemini_api_key.strip()
            if k and k not in seen:
                keys.append(k)
        return keys

    def _build_model_list(self) -> list[str]:
        models = [self.model, "gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]
        seen: set[str] = set()
        unique = []
        for m in models:
            if m not in seen:
                seen.add(m)
                unique.append(m)
        return unique

    async def _gemini_generate_async(self, prompt: str) -> str:
        if not self._api_keys:
            raise LLMClientError("No GEMINI_API_KEY or GEMINI_API_KEYS configured")

        unique_models = self._build_model_list()
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

        async with httpx.AsyncClient(timeout=40.0) as client:
            for api_key in self._api_keys:
                for model_name in unique_models:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
                    headers = {
                        "Content-Type": "application/json",
                        "x-goog-api-key": api_key,
                    }
                    try:
                        response = await client.post(url, json=payload, headers=headers)
                        if response.status_code == 429:
                            last_error = f"key ...{api_key[-4:]}/{model_name}: quota exhausted"
                            logger.warning(last_error)
                            break  # skip to next key
                        response.raise_for_status()
                        data = response.json()
                        candidates = data.get("candidates") or []
                        if not candidates:
                            last_error = f"key ...{api_key[-4:]}/{model_name}: no candidates"
                            continue
                        parts = candidates[0].get("content", {}).get("parts", [])
                        text = "".join(
                            p.get("text", "") for p in parts if isinstance(p, dict)
                        ).strip()
                        if text:
                            return text
                        last_error = f"key ...{api_key[-4:]}/{model_name}: empty text"
                    except httpx.HTTPStatusError as exc:
                        if exc.response.status_code == 429:
                            last_error = f"key ...{api_key[-4:]}/{model_name}: quota exhausted"
                            logger.warning(last_error)
                            break
                        last_error = f"key ...{api_key[-4:]}/{model_name}: HTTP {exc.response.status_code}"
                        continue
                    except Exception as exc:
                        last_error = f"key ...{api_key[-4:]}/{model_name}: {exc}"
                        continue

        raise LLMClientError(
            f"Gemini generation failed after trying {len(self._api_keys)} key(s): {last_error}"
        )

    def _gemini_generate(self, prompt: str) -> str:
        """Synchronous wrapper — use generate_async when possible."""
        if not self._api_keys:
            raise LLMClientError("No GEMINI_API_KEY or GEMINI_API_KEYS configured")

        unique_models = self._build_model_list()
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
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
                    headers = {
                        "Content-Type": "application/json",
                        "x-goog-api-key": api_key,
                    }
                    try:
                        response = client.post(url, json=payload, headers=headers)
                        if response.status_code == 429:
                            last_error = f"key ...{api_key[-4:]}/{model_name}: quota exhausted"
                            break
                        response.raise_for_status()
                        data = response.json()
                        candidates = data.get("candidates") or []
                        if not candidates:
                            last_error = f"key ...{api_key[-4:]}/{model_name}: no candidates"
                            continue
                        parts = candidates[0].get("content", {}).get("parts", [])
                        text = "".join(
                            p.get("text", "") for p in parts if isinstance(p, dict)
                        ).strip()
                        if text:
                            return text
                        last_error = f"key ...{api_key[-4:]}/{model_name}: empty text"
                    except httpx.HTTPStatusError as exc:
                        if exc.response.status_code == 429:
                            last_error = f"key ...{api_key[-4:]}/{model_name}: quota exhausted"
                            break
                        last_error = f"key ...{api_key[-4:]}/{model_name}: HTTP {exc.response.status_code}"
                        continue
                    except Exception as exc:
                        last_error = f"key ...{api_key[-4:]}/{model_name}: {exc}"
                        continue

        raise LLMClientError(
            f"Gemini generation failed after trying {len(self._api_keys)} key(s): {last_error}"
        )

    def generate(self, prompt: str) -> str:
        if self.provider == "gemini":
            return self._gemini_generate(prompt)
        raise LLMClientError(f"Unsupported LLM provider: {self.provider}")

    async def generate_async(self, prompt: str) -> str:
        if self.provider == "gemini":
            return await self._gemini_generate_async(prompt)
        raise LLMClientError(f"Unsupported LLM provider: {self.provider}")
