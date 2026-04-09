from dataclasses import dataclass, field
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = "AI Summarizer API"
    app_version: str = "0.1.0"
    cors_origins: list[str] = field(
        default_factory=lambda: [
            origin.strip()
            for origin in os.getenv("CORS_ORIGINS", "http://127.0.0.1:5500").split(",")
            if origin.strip()
        ]
    )


settings = Settings()
