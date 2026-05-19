from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from backend.app.config import settings
from backend.app.contracts import SceneRecipe


class GenerationResult(BaseModel):
    success: bool
    output_path: Path | None = None
    backend: str = "diffusers"
    model_id: str
    device: str
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


def _prompt(recipe: SceneRecipe) -> str:
    return " ".join(
        [
            recipe.compiled_prompt,
            "adult editorial model",
            "luxury catalog campaign still",
            "product area left empty or placeholder-free",
            "no visible brand logos",
        ]
    )


def _load_pipeline(model_id: str) -> Any:
    if "FLUX" in model_id.upper():
        from diffusers import FluxPipeline

        return FluxPipeline.from_pretrained(model_id)  # type: ignore[no-untyped-call]

    try:
        from diffusers import AutoPipelineForText2Image

        return AutoPipelineForText2Image.from_pretrained(model_id)  # type: ignore[no-untyped-call]
    except (ImportError, AttributeError):
        from diffusers import DiffusionPipeline

        return DiffusionPipeline.from_pretrained(model_id)  # type: ignore[no-untyped-call]


def _invoke_pipeline(pipe: Any, recipe: SceneRecipe, generator: Any) -> Any:
    kwargs: dict[str, Any] = {
        "prompt": _prompt(recipe),
        "width": settings.image_width,
        "height": settings.image_height,
        "num_inference_steps": settings.image_steps,
        "guidance_scale": settings.image_guidance_scale,
        "generator": generator,
    }

    try:
        import inspect

        signature = inspect.signature(pipe.__call__)
        if "negative_prompt" in signature.parameters:
            kwargs["negative_prompt"] = recipe.negative_prompt
    except (TypeError, ValueError):
        pass

    return pipe(**kwargs)


def generate_hero_still_with_diffusers(
    recipe: SceneRecipe,
    output_path: Path,
) -> GenerationResult:
    model_id = settings.image_model_id
    device = resolve_device()
    dependency_status = generation_dependency_status()

    try:
        import torch
    except ImportError as exc:
        return GenerationResult(
            success=False,
            output_path=None,
            model_id=model_id,
            device=device,
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

        pipe = _load_pipeline(model_id)
        pipe = pipe.to(device)
        generator_device = device if device in {"cuda", "cpu"} else "cpu"
        generator = torch.Generator(device=generator_device).manual_seed(recipe.seed)
        result = _invoke_pipeline(pipe, recipe, generator)
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
            dependency_status=dependency_status,
            notes=[
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
        dependency_status=dependency_status,
        notes=[*notes, "Real hero still generated with Diffusers."],
        error=None,
    )
