from typing import List
from pydantic_settings import BaseSettings


def _parse_list_setting(value: str) -> List[str]:
    """
    Parses a setting that should be a list of strings, accepting either:
      - a plain comma-separated string (what Render's env var UI stores
        naturally, e.g. https://foo.com,https://bar.com), or
      - a JSON array string (e.g. ["https://foo.com","https://bar.com"])

    NOTE: these settings are deliberately declared as plain `str` fields
    below, NOT List[str]. pydantic-settings auto-JSON-decodes env vars for
    any field typed as a list/complex type, at the settings-SOURCE level,
    before any field validator gets a chance to run -- so a plain
    comma-separated value (no brackets/quotes) would always raise a
    SettingsError before you could even intercept it. Keeping the field
    as `str` avoids that entirely, and this helper parses it afterward.
    """
    stripped = (value or "").strip()
    if not stripped:
        return []
    if stripped.startswith("["):
        import json
        try:
            return json.loads(stripped)
        except Exception:
            pass
    return [item.strip() for item in stripped.split(",") if item.strip()]


class Settings(BaseSettings):

    # Application
    APP_NAME: str = "RecruitIQ"
    APP_VERSION: str = "1.0.0"

    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = False

    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    API_PREFIX: str = "/api"

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres123@localhost:5432/recruitiq"
    DATABASE_ECHO: bool = False

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # Security
    SECRET_KEY: str = "RecruitIQ_Development_Secret_Key_2026"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    JWT_REFRESH_EXPIRATION_DAYS: int = 7

    # CORS -- stored as plain comma-separated strings (see
    # _parse_list_setting above for why), exposed as lists via the
    # @property accessors below. Use settings.cors_origins_list (etc.)
    # everywhere in the app, NOT these raw fields directly.
    CORS_ORIGINS: str = (
        "http://localhost:3000,http://localhost:5173,"
        "http://127.0.0.1:3000,http://127.0.0.1:5173"
    )
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: str = "*"
    CORS_HEADERS: str = "*"

    ALLOWED_HOSTS: str = "localhost,127.0.0.1"
    # Note: add your production domain(s) here (or via the ALLOWED_HOSTS
    # env var) once deployed. A "*" wildcard was here before, which made
    # TrustedHostMiddleware a no-op -- it accepted literally any Host
    # header, defeating the point of the check.

    # OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""

    # AWS
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    AWS_S3_BUCKET: str = "recruitiq-resumes"

    # AI/ML
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4"
    HUGGINGFACE_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    CEREBRAS_API_KEY: str = ""
    TOGETHER_API_KEY: str = ""
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587

    SMTP_EMAIL: str = ""
    SMTP_PASSWORD: str = ""
    # File Upload
    MAX_UPLOAD_SIZE: int = 10485760

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100

    # Features
    ENABLE_BIAS_DETECTION: bool = True
    ENABLE_SALARY_ESTIMATION: bool = True
    ENABLE_INTERVIEW_QUESTIONS: bool = True

    @property
    def cors_origins_list(self) -> List[str]:
        return _parse_list_setting(self.CORS_ORIGINS)

    @property
    def cors_methods_list(self) -> List[str]:
        return _parse_list_setting(self.CORS_METHODS)

    @property
    def cors_headers_list(self) -> List[str]:
        return _parse_list_setting(self.CORS_HEADERS)

    @property
    def allowed_hosts_list(self) -> List[str]:
        return _parse_list_setting(self.ALLOWED_HOSTS)

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()