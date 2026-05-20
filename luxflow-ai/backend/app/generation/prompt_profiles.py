from pydantic import BaseModel

from backend.app.contracts import SceneRecipe

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
    notes: list[str]


def _product_empty_action_name(action_name: str) -> str:
    normalized = action_name.lower().replace("_", " ")
    normalized = normalized.replace("with handbag", "with natural hand placement")
    normalized = normalized.replace("with bag", "with natural hand placement")
    return normalized


def build_hero_still_prompt(recipe: SceneRecipe, profile_id: str) -> PromptBundle:
    positive_parts = [
        "luxury catalog still",
        f"adult {recipe.model.gender_presentation} editorial model",
        f"in a {recipe.location.name}",
        f"{recipe.location.lighting} lighting",
        f"{recipe.location.mood} mood",
        f"action: {_product_empty_action_name(recipe.action.name)}",
        "natural hands for later product placement",
        "empty space near one hand for product compositing",
        "no prominent bag",
        "no branded accessory",
        "no logos",
        "product composited later",
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
        "prominent handbag",
        "branded accessory",
        "logo text",
        "unrealistic hands",
    ]

    return PromptBundle(
        positive_prompt=", ".join(positive_parts),
        negative_prompt=", ".join(negative_parts),
        notes=[
            f"Prompt profile: {profile_id}",
            "Hero still is a product-empty scene canvas for later compositing.",
            "Prompt avoids generating the exact handbag.",
        ],
    )
