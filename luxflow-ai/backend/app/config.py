from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for local-first development."""

    env: str = "development"
    assets_dir: Path = Path("assets")
    output_root: Path = Path("assets/outputs")
    catalog_path: Path = Path("assets/catalog/sample_catalog.json")
    database_url: str = "sqlite:///./luxflow.db"
    enable_hosted_fallback: bool = False
    enable_real_image_generation: bool = False
    image_generation_backend: str = "diffusers"
    image_profile_id: str = ""
    image_prompt_variant_id: str = "editorial_empty_hand_v1"
    image_model_id: str = "black-forest-labs/FLUX.1-schnell"
    image_device: str = "auto"
    image_width: int = 1024
    image_height: int = 1024
    image_steps: int = 4
    image_guidance_scale: float = 0.0

    model_config = SettingsConfigDict(env_prefix="LUXFLOW_", env_file=".env", extra="ignore")


settings = Settings()


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def resolve_project_path(path: Path) -> Path:
    return path if path.is_absolute() else project_root() / path
