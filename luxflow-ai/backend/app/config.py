from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for local-first development."""

    env: str = "development"
    assets_dir: Path = Path("assets")
    catalog_path: Path = Path("assets/catalog/sample_catalog.json")
    database_url: str = "sqlite:///./luxflow.db"
    enable_hosted_fallback: bool = False

    model_config = SettingsConfigDict(env_prefix="LUXFLOW_", env_file=".env", extra="ignore")


settings = Settings()


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def resolve_project_path(path: Path) -> Path:
    return path if path.is_absolute() else project_root() / path
