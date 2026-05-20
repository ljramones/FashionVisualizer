from backend.app.config import settings
from backend.app.contracts import SystemCapabilities
from backend.app.generation.diffusers_hero_still import (
    generation_dependencies_available,
    probe_torch_devices,
    resolve_device,
)
from backend.app.generation.model_candidates import get_model_candidates


def get_system_capabilities() -> dict[str, object]:
    """Return conservative placeholder capabilities until engines are installed."""

    capabilities = SystemCapabilities().model_dump(mode="json")
    devices = probe_torch_devices()
    capabilities.update(
        {
            "real_image_generation_enabled": settings.enable_real_image_generation,
            "image_generation_backend": settings.image_generation_backend,
            "image_model_id": settings.image_model_id,
            "generation_dependencies_available": generation_dependencies_available(),
            "mps_available": devices["mps_available"],
            "cuda_available": devices["cuda_available"],
            "selected_generation_device": resolve_device(),
            "candidate_model_count": len(get_model_candidates()),
            "default_model_id": settings.image_model_id,
        }
    )
    return capabilities
