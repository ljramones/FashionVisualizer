import hashlib
import json

from backend.app.contracts import GenerationRequest, SceneRecipe
from backend.app.recipes.prompt_templates import BASE_HANDBAG_PROMPT, NEGATIVE_PROMPT
from backend.app.registry.asset_registry import get_action, get_location, get_model, get_product


def request_hash(request: GenerationRequest) -> str:
    """Hash normalized public request fields for deterministic cache keys."""

    normalized = {
        "product_id": request.product_id,
        "model_id": request.model_id,
        "location_id": request.location_id,
        "action_id": request.action_id,
        "seed": request.seed,
        "aspect_ratio": request.aspect_ratio,
        "mode": request.mode.value,
    }
    payload = json.dumps(normalized, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def compile_scene_recipe(request: GenerationRequest) -> SceneRecipe:
    product = get_product(request.product_id)
    model = get_model(request.model_id)
    location = get_location(request.location_id)
    action = get_action(request.action_id)

    compiled_prompt = " ".join(
        [
            BASE_HANDBAG_PROMPT,
            f"Feature {product.name}: {product.description}",
            f"Model profile: {model.display_name}.",
            location.prompt_fragment,
            f"Lighting: {location.lighting}. Mood: {location.mood}.",
            action.prompt_fragment,
            f"Camera motion: {action.camera_motion}.",
            f"Product interaction: {action.product_interaction}.",
            f"Aspect ratio {request.aspect_ratio}.",
        ]
    )

    return SceneRecipe(
        product=product,
        model=model,
        location=location,
        action=action,
        compiled_prompt=compiled_prompt,
        negative_prompt=NEGATIVE_PROMPT,
        route_hint=f"{product.category.value}:{request.mode.value}",
        request_hash=request_hash(request),
        seed=request.seed,
        aspect_ratio=request.aspect_ratio,
        mode=request.mode,
    )
