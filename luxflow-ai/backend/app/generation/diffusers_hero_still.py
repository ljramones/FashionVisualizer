from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from backend.app.config import settings
from backend.app.contracts import SceneRecipe
from backend.app.generation.dimensions import resolve_generation_dimensions
from backend.app.generation.image_profiles import ImageGenerationProfile, resolve_image_profile
from backend.app.generation.prompt_profiles import PromptBundle, build_hero_still_prompt


class GenerationResult(BaseModel):
    success: bool
    output_path: Path | None = None
    backend: str = "diffusers"
    model_id: str
    device: str
    profile_id: str | None = None
    width: int | None = None
    height: int | None = None
    steps: int | None = None
    guidance_scale: float | None = None
    supports_negative_prompt: bool | None = None
    positive_prompt_preview: str | None = None
    negative_prompt_preview: str | None = None
    prompt_variant_id: str | None = None
    composition_target_summary: str | None = None
    final_catalog_action_label: str | None = None
    hero_action_prompt_used: str | None = None
    forbidden_generated_objects: list[str] = Field(default_factory=list)
    no_accessory_strategy: bool = False
    aspect_ratio_requested: str | None = None
    aspect_ratio_resolved: str | None = None
    prompt_strategy: str = "product_empty_scene_for_later_composite"
    prompt_profile_used: str | None = None
    dependency_status: dict[str, object] = Field(default_factory=dict)
    notes: list[str]
    error: str | None = None


def generation_dependency_status() -> dict[str, object]:
    status: dict[str, object] = {
        "torch_available": False,
        "diffusers_available": False,
        "torch_version": None,
        "diffusers_version": None,
        "mps_available": False,
        "cuda_available": False,
    }

    try:
        import torch

        status["torch_available"] = True
        status["torch_version"] = getattr(torch, "__version__", "unknown")
        status["mps_available"] = bool(
            hasattr(torch.backends, "mps") and torch.backends.mps.is_available()
        )
        status["cuda_available"] = bool(torch.cuda.is_available())
    except ImportError:
        pass

    try:
        import diffusers

        status["diffusers_available"] = True
        status["diffusers_version"] = getattr(diffusers, "__version__", "unknown")
    except ImportError:
        pass

    return status


def generation_dependencies_available() -> bool:
    status = generation_dependency_status()
    return bool(status["torch_available"] and status["diffusers_available"])


def probe_torch_devices() -> dict[str, bool]:
    status = generation_dependency_status()
    return {
        "mps_available": bool(status["mps_available"]),
        "cuda_available": bool(status["cuda_available"]),
    }


def resolve_device() -> str:
    if settings.image_device != "auto":
        return settings.image_device

    devices = probe_torch_devices()
    if devices["mps_available"]:
        return "mps"
    if devices["cuda_available"]:
        return "cuda"
    return "cpu"


def _preview(text: str, limit: int = 500) -> str:
    return text if len(text) <= limit else f"{text[:limit].rstrip()}..."


def _aspect_ratio(width: int, height: int) -> str:
    return "1:1" if width == height else "9:16" if height > width else "custom"


def _requested_dimensions(profile_id: str) -> tuple[int | None, int | None]:
    if profile_id and settings.image_width == 1024 and settings.image_height == 1024:
        return None, None
    return settings.image_width, settings.image_height


def _resolve_profile() -> ImageGenerationProfile:
    return resolve_image_profile(settings.image_profile_id or None, settings.image_model_id)


def _resolve_generation_parameters(recipe: SceneRecipe) -> tuple[
    ImageGenerationProfile,
    PromptBundle,
    int,
    int,
    int,
    float,
]:
    profile = _resolve_profile()
    requested_width, requested_height = _requested_dimensions(profile.profile_id)
    width, height = resolve_generation_dimensions(
        recipe.aspect_ratio,
        profile.profile_id,
        recipe.mode.value,
        requested_width=requested_width,
        requested_height=requested_height,
    )
    steps = settings.image_steps if settings.image_steps != 4 else profile.default_steps
    guidance_scale = (
        settings.image_guidance_scale
        if settings.image_guidance_scale != 0.0
        else profile.default_guidance_scale
    )
    prompt_bundle = build_hero_still_prompt(
        recipe,
        profile.profile_id,
        settings.image_prompt_variant_id,
    )
    return profile, prompt_bundle, width, height, steps, guidance_scale


def _pipeline_load_kwargs(device: str) -> dict[str, Any]:
    try:
        import torch
    except ImportError:
        return {}

    if device in {"cpu", "mps"}:
        return {"torch_dtype": torch.float32}
    if device == "cuda":
        return {"torch_dtype": torch.float16}
    return {}


def _load_pipeline(model_id: str, device: str) -> Any:
    kwargs = _pipeline_load_kwargs(device)
    if "FLUX" in model_id.upper():
        from diffusers import FluxPipeline

        return FluxPipeline.from_pretrained(model_id, **kwargs)  # type: ignore[no-untyped-call]

    try:
        from diffusers import AutoPipelineForText2Image

        return AutoPipelineForText2Image.from_pretrained(model_id, **kwargs)  # type: ignore[no-untyped-call]
    except (ImportError, AttributeError):
        from diffusers import DiffusionPipeline

        return DiffusionPipeline.from_pretrained(model_id, **kwargs)  # type: ignore[no-untyped-call]


def _invoke_pipeline(
    pipe: Any,
    prompt_bundle: PromptBundle,
    generator: Any,
    width: int,
    height: int,
    steps: int,
    guidance_scale: float,
    supports_negative_prompt: bool,
) -> Any:
    kwargs: dict[str, Any] = {
        "prompt": prompt_bundle.positive_prompt,
        "width": width,
        "height": height,
        "num_inference_steps": steps,
        "guidance_scale": guidance_scale,
        "generator": generator,
    }

    try:
        import inspect

        signature = inspect.signature(pipe.__call__)
        if supports_negative_prompt and "negative_prompt" in signature.parameters:
            kwargs["negative_prompt"] = prompt_bundle.negative_prompt
    except (TypeError, ValueError):
        pass

    return pipe(**kwargs)


def generate_hero_still_with_diffusers(
    recipe: SceneRecipe,
    output_path: Path,
) -> GenerationResult:
    profile, prompt_bundle, width, height, steps, guidance_scale = (
        _resolve_generation_parameters(recipe)
    )
    model_id = profile.model_id if settings.image_profile_id else settings.image_model_id
    device = resolve_device()
    dependency_status = generation_dependency_status()
    metadata: dict[str, Any] = {
        "profile_id": profile.profile_id,
        "width": width,
        "height": height,
        "steps": steps,
        "guidance_scale": guidance_scale,
        "supports_negative_prompt": profile.supports_negative_prompt,
        "positive_prompt_preview": _preview(prompt_bundle.positive_prompt),
        "negative_prompt_preview": _preview(prompt_bundle.negative_prompt),
        "prompt_variant_id": prompt_bundle.prompt_variant_id,
        "composition_target_summary": prompt_bundle.composition_target_summary,
        "final_catalog_action_label": prompt_bundle.final_catalog_action_label,
        "hero_action_prompt_used": prompt_bundle.hero_action_prompt_used,
        "forbidden_generated_objects": prompt_bundle.forbidden_generated_objects,
        "no_accessory_strategy": prompt_bundle.no_accessory_strategy,
        "aspect_ratio_requested": recipe.aspect_ratio,
        "aspect_ratio_resolved": _aspect_ratio(width, height),
        "prompt_profile_used": profile.profile_id,
        "prompt_strategy": "product_empty_scene_for_later_composite",
    }

    try:
        import torch
    except ImportError as exc:
        return GenerationResult(
            success=False,
            output_path=None,
            model_id=model_id,
            device=device,
            **metadata,
            dependency_status=dependency_status,
            notes=[
                "Real image generation requested, but torch is not installed.",
                "Install optional dependencies with pip install -e \".[dev,generation]\".",
            ],
            error=str(exc),
        )

    try:
        import diffusers  # noqa: F401
    except ImportError as exc:
        return GenerationResult(
            success=False,
            output_path=None,
            model_id=model_id,
            device=device,
            **metadata,
            dependency_status=dependency_status,
            notes=[
                "Real image generation requested, but diffusers is not installed.",
                "Falling back to deterministic placeholder hero still.",
            ],
            error=str(exc),
        )

    pipe: Any | None = None
    result: Any | None = None
    tmp_path = output_path.with_name(f"{output_path.stem}.tmp{output_path.suffix}")

    try:
        notes = []
        if device == "cpu":
            notes.append("Using CPU device; real generation may be slow.")
        if device == "mps":
            notes.append("Using Apple Metal/MPS device for local generation.")
        if device == "cuda":
            notes.append("Using CUDA device for local generation.")

        pipe = _load_pipeline(model_id, device)
        pipe = pipe.to(device)
        generator_device = device if device in {"cuda", "cpu"} else "cpu"
        generator = torch.Generator(device=generator_device).manual_seed(recipe.seed)
        result = _invoke_pipeline(
            pipe,
            prompt_bundle,
            generator,
            width,
            height,
            steps,
            guidance_scale,
            profile.supports_negative_prompt,
        )
        image = result.images[0]
        output_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(tmp_path)
        tmp_path.replace(output_path)
    except Exception as exc:  # noqa: BLE001 - fallback path must catch backend failures.
        if tmp_path.exists():
            tmp_path.unlink()
        return GenerationResult(
            success=False,
            output_path=None,
            model_id=model_id,
            device=device,
            **metadata,
            dependency_status=dependency_status,
            notes=[
                *prompt_bundle.notes,
                "Diffusers generation failed or model access was unavailable.",
                "Falling back to deterministic placeholder hero still.",
            ],
            error=str(exc),
        )
    finally:
        pipe = None
        result = None
        try:
            import gc

            gc.collect()
            if device == "cuda" and hasattr(torch, "cuda"):
                torch.cuda.empty_cache()
            if device == "mps" and hasattr(torch, "mps") and hasattr(torch.mps, "empty_cache"):
                torch.mps.empty_cache()
        except Exception:
            pass

    return GenerationResult(
        success=True,
        output_path=output_path,
        model_id=model_id,
        device=device,
        **metadata,
        dependency_status=dependency_status,
        notes=[*prompt_bundle.notes, *notes, "Real hero still generated with Diffusers."],
        error=None,
    )
