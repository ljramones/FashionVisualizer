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
    "handbag",
    "bag",
    "purse",
    "tote",
    "clutch",
    "luggage",
    "shopping bag",
    "backpack",
    "strap",
    "chain strap",
    "branded accessory",
    "object in hand",
    "fake fashion accessory",
]


class PromptBundle(BaseModel):
    positive_prompt: str
    negative_prompt: str
    prompt_variant_id: str
    composition_target_summary: str
    hero_action_prompt_used: str
    final_catalog_action_label: str
    forbidden_generated_objects: list[str]
    no_accessory_strategy: bool
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


def _hero_action_prompt(recipe: SceneRecipe) -> str:
    if recipe.action.hero_action_prompt_fragment:
        return recipe.action.hero_action_prompt_fragment
    return (
        f"adult editorial model {_product_empty_action_name(recipe.action.name)}, "
        "empty hands visible, clear placement space near the side"
    )


def _final_catalog_label(recipe: SceneRecipe) -> str:
    return recipe.action.final_catalog_action_label or recipe.action.name.lower()


def _forbidden_objects(recipe: SceneRecipe) -> list[str]:
    defaults = [
        "handbag",
        "bag",
        "purse",
        "tote",
        "clutch",
        "luggage",
        "shopping bag",
        "backpack",
        "strap",
        "chain strap",
        "branded accessory",
    ]
    merged = [*defaults, *recipe.action.forbidden_generated_objects]
    return list(dict.fromkeys(term for term in merged if term))


def build_hero_still_prompt(
    recipe: SceneRecipe,
    profile_id: str,
    prompt_variant_id: str | None = None,
) -> PromptBundle:
    variant = resolve_prompt_variant(prompt_variant_id)
    composition_target = _composition_target_summary(recipe)
    hero_action_prompt = _hero_action_prompt(recipe)
    forbidden_objects = _forbidden_objects(recipe)
    positive_parts = [
        "luxury catalog editorial photo",
        f"adult {recipe.model.gender_presentation} model in {recipe.location.name}",
        f"{recipe.location.lighting.split(' with ')[0]}, {recipe.location.mood.split(',')[0]}",
        hero_action_prompt,
        "empty visible hands, clean right-side blank placement zone",
        "accessory-free styling, logo-free wardrobe",
        *variant.positive_additions[:1],
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
        *forbidden_objects,
        *variant.negative_additions,
        "prominent handbag",
        "branded accessory",
        "logo text",
        "unrealistic hands",
    ]

    return PromptBundle(
        positive_prompt=", ".join(positive_parts),
        negative_prompt=", ".join(dict.fromkeys(negative_parts)),
        prompt_variant_id=variant.variant_id,
        composition_target_summary=composition_target,
        hero_action_prompt_used=hero_action_prompt,
        final_catalog_action_label=_final_catalog_label(recipe),
        forbidden_generated_objects=forbidden_objects,
        no_accessory_strategy=True,
        notes=[
            f"Prompt profile: {profile_id}",
            f"Prompt variant: {variant.variant_id}",
            f"Variant use: {variant.intended_use}",
            "Hero still is a product-empty scene canvas for later compositing.",
            "Hero-stage action is decoupled from the final catalog action.",
            "Prompt avoids generating the exact handbag.",
            *variant.notes,
        ],
    )
