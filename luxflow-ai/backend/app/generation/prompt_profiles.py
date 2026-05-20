from pydantic import BaseModel

from backend.app.contracts import SceneRecipe
from backend.app.generation.prompt_variants import resolve_prompt_variant

PRODUCT_PRESERVATION_NEGATIVE_TERMS = [
    "distorted bag",
    "warped product",
    "changed logo",
    "extra straps",
    "floating object",
    "broken hands",
    "deformed fingers",
    "flicker",
    "text",
    "watermark",
    "duplicate accessories",
    "fake brand logo",
    "malformed handbag",
]


class PromptBundle(BaseModel):
    positive_prompt: str
    negative_prompt: str
    prompt_variant_id: str
    composition_target_summary: str
    notes: list[str]


def _product_empty_action_name(action_name: str) -> str:
    normalized = action_name.lower().replace("_", " ")
    normalized = normalized.replace("with handbag", "with natural hand placement")
    normalized = normalized.replace("with bag", "with natural hand placement")
    return normalized


def _composition_target_summary(recipe: SceneRecipe) -> str:
    target = recipe.action.product_anchor_target or "right_hand"
    space = recipe.action.composition_space_hint or (
        "clear empty space near the model hand for later handbag placement"
    )
    occlusion = recipe.action.occlusion_hint or (
        "hand visible, relaxed fingers, no object currently held"
    )
    return f"{target}: {space}. {occlusion}."


def _composition_prompt_phrase(recipe: SceneRecipe) -> str:
    target = recipe.action.product_anchor_target or "right_hand"
    readable_target = target.replace("_", " ")
    return f"{readable_target} clear, relaxed visible fingers, no object held"


def build_hero_still_prompt(
    recipe: SceneRecipe,
    profile_id: str,
    prompt_variant_id: str | None = None,
) -> PromptBundle:
    variant = resolve_prompt_variant(prompt_variant_id)
    composition_target = _composition_target_summary(recipe)
    positive_parts = [
        "luxury catalog still",
        f"adult {recipe.model.gender_presentation} editorial model",
        recipe.location.name,
        recipe.location.lighting.split(" with ")[0],
        recipe.location.mood.split(",")[0],
        f"action: {_product_empty_action_name(recipe.action.name)}",
        _composition_prompt_phrase(recipe),
        "no prominent bag",
        "no purse",
        "no branded accessory",
        "no logos",
        "product composited later",
        *variant.positive_additions[:2],
    ]

    if profile_id == "sdxl_base_quality":
        positive_parts.extend(
            [
                f"camera: {recipe.action.camera_motion}",
                "polished commercial fashion photography",
            ]
        )

    negative_parts = [
        *PRODUCT_PRESERVATION_NEGATIVE_TERMS,
        *variant.negative_additions,
        "prominent handbag",
        "branded accessory",
        "logo text",
        "unrealistic hands",
    ]

    return PromptBundle(
        positive_prompt=", ".join(positive_parts),
        negative_prompt=", ".join(negative_parts),
        prompt_variant_id=variant.variant_id,
        composition_target_summary=composition_target,
        notes=[
            f"Prompt profile: {profile_id}",
            f"Prompt variant: {variant.variant_id}",
            f"Variant use: {variant.intended_use}",
            "Hero still is a product-empty scene canvas for later compositing.",
            "Prompt avoids generating the exact handbag.",
            *variant.notes,
        ],
    )
