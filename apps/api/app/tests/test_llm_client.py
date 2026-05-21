"""Tests for LLM client module."""
import pytest

from app.services.llm_client import LLMClient, LLMClientError


def test_no_keys_raises():
    import app.core.config as config_mod
    orig_key = config_mod.settings.gemini_api_key
    orig_keys = config_mod.settings.gemini_api_keys
    try:
        config_mod.settings.gemini_api_key = ""
        config_mod.settings.gemini_api_keys = ""
        client = LLMClient()
        with pytest.raises(LLMClientError, match="No GEMINI_API_KEY"):
            client.generate("test")
    finally:
        config_mod.settings.gemini_api_key = orig_key
        config_mod.settings.gemini_api_keys = orig_keys


def test_unsupported_provider_raises():
    import app.core.config as config_mod
    orig = config_mod.settings.llm_provider
    try:
        config_mod.settings.llm_provider = "openai"
        client = LLMClient()
        with pytest.raises(LLMClientError, match="Unsupported"):
            client.generate("test")
    finally:
        config_mod.settings.llm_provider = orig


def test_collect_keys_deduplicates():
    import app.core.config as config_mod
    orig_key = config_mod.settings.gemini_api_key
    orig_keys = config_mod.settings.gemini_api_keys
    try:
        config_mod.settings.gemini_api_key = "key-a"
        config_mod.settings.gemini_api_keys = "key-a,key-b,key-a"
        client = LLMClient()
        assert client._api_keys == ["key-a", "key-b"]
    finally:
        config_mod.settings.gemini_api_key = orig_key
        config_mod.settings.gemini_api_keys = orig_keys


def test_model_list_deduplicates():
    client = LLMClient()
    models = client._build_model_list()
    assert len(models) == len(set(models))
    assert models[0] == client.model
