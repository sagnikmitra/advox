"""Tests for JWT auth module."""
from app.core.auth import _decode_supabase_jwt


def test_decode_returns_none_without_secret():
    """Without jwt_secret configured, local decode should return None."""
    import app.core.config as config_mod
    original = config_mod.settings.supabase_jwt_secret
    try:
        config_mod.settings.supabase_jwt_secret = ""
        result = _decode_supabase_jwt("fake.token.here")
        assert result is None
    finally:
        config_mod.settings.supabase_jwt_secret = original


def test_decode_returns_none_for_invalid_token():
    """With a secret but garbage token, should return None (not raise)."""
    import app.core.config as config_mod
    original = config_mod.settings.supabase_jwt_secret
    try:
        config_mod.settings.supabase_jwt_secret = "test-secret-key"
        result = _decode_supabase_jwt("not.a.valid.jwt")
        assert result is None
    finally:
        config_mod.settings.supabase_jwt_secret = original
