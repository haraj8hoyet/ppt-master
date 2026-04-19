"""Configuration loader for ppt-master."""

import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    openai_model: str = field(default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    openai_base_url: str = field(default_factory=lambda: os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"))
    max_slides: int = field(default_factory=lambda: int(os.getenv("MAX_SLIDES", "15")))
    default_theme: str = field(default_factory=lambda: os.getenv("DEFAULT_THEME", "dark"))
    output_dir: str = field(default_factory=lambda: os.getenv("OUTPUT_DIR", "output"))
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

    def validate(self) -> list[str]:
        """Return a list of validation error messages."""
        errors: list[str] = []
        if not self.openai_api_key:
            errors.append("OPENAI_API_KEY is required but not set.")
        if self.max_slides < 1 or self.max_slides > 50:
            errors.append("MAX_SLIDES must be between 1 and 50.")
        if self.default_theme not in ("default", "dark", "light", "corporate"):
            errors.append(f"DEFAULT_THEME '{self.default_theme}' is not a recognised theme.")
        return errors


_config: Config | None = None


def get_config() -> Config:
    """Return the singleton Config instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config
