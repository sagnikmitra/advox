from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Advox API"
    api_prefix: str = "/api"
    legal_transition_date: str = "2024-07-01"
    database_url: str = ""
    redis_url: str = "redis://localhost:6379/0"
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_secret_key: str = ""
    supabase_jwt_secret: str = ""
    llm_provider: str = "gemini"
    llm_model: str = "gemini-2.0-flash"
    gemini_api_key: str = ""
    gemini_api_keys: str = ""
    basic_auth_enabled: bool = False
    basic_auth_user: str = "admin"
    basic_auth_password: str = "change-me"


settings = Settings()
