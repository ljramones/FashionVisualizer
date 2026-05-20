from pydantic import BaseModel


class HeroPromptVariant(BaseModel):
    variant_id: str
    intended_use: str
    positive_additions: list[str]
    negative_additions: list[str]
    notes: list[str]


PROMPT_VARIANTS: tuple[HeroPromptVariant, ...] = (
    HeroPromptVariant(
        variant_id="strict_empty_hand_no_accessory_v1",
        intended_use="Strongest no-accessory prompt for hero stills before product compositing.",
        positive_additions=[
            "empty hands clearly visible",
            "no object held",
            "accessory-free silhouette",
            "clean right side placement zone",
            "relaxed fingers",
            "visible hand near hip",
            "product placement zone left blank",
        ],
        negative_additions=[
            "handbag",
            "purse",
            "bag",
            "tote",
            "clutch",
            "luggage",
            "backpack",
            "shopping bag",
            "strap",
            "chain strap",
            "object in hand",
            "fake fashion accessory",
            "branded accessory",
        ],
        notes=["Use when the model keeps hallucinating purses or side-carry accessories."],
    ),
    HeroPromptVariant(
        variant_id="editorial_empty_hand_v1",
        intended_use="Strongest product-empty instruction for later handbag compositing.",
        positive_additions=[
            "empty right hand",
            "right hand visible and relaxed",
            "clear product placement space by right hip",
            "no object currently held",
        ],
        negative_additions=[
            "bag",
            "purse",
            "handbag",
            "luggage",
            "object in hand",
            "covered hand",
        ],
        notes=["Best first choice for product-locked handbag insertion."],
    ),
    HeroPromptVariant(
        variant_id="natural_side_carry_space_v1",
        intended_use="Walking pose with natural side space near the hand and hip.",
        positive_additions=[
            "walking naturally",
            "right arm relaxed near side",
            "visible right hip area",
            "open space beside the body",
        ],
        negative_additions=[
            "crossed arms",
            "hidden hands",
            "busy foreground",
            "purse",
            "bag strap",
        ],
        notes=["Targets later side-carry handbag placement."],
    ),
    HeroPromptVariant(
        variant_id="minimal_accessory_free_v1",
        intended_use="Avoid generated accessories, logos, and extra objects.",
        positive_additions=[
            "clean minimalist styling",
            "accessory-free outfit",
            "simple silhouette",
            "uncluttered product placement area",
        ],
        negative_additions=[
            "purse",
            "bag",
            "luggage",
            "jewelry clutter",
            "logo",
            "brand mark",
            "shopping bag",
        ],
        notes=["Useful when models hallucinate unwanted accessories."],
    ),
    HeroPromptVariant(
        variant_id="luxury_campaign_motion_v1",
        intended_use="More cinematic catalog framing while preserving product space.",
        positive_additions=[
            "cinematic luxury campaign",
            "soft motion energy",
            "premium editorial framing",
            "negative space near right hand",
        ],
        negative_additions=[
            "motion blur on hands",
            "bag",
            "purse",
            "fake logo",
            "text overlay",
        ],
        notes=["Use when composition is too static."],
    ),
    HeroPromptVariant(
        variant_id="studio_safe_pose_v1",
        intended_use="Simple safe pose for easier product compositing.",
        positive_additions=[
            "simple upright pose",
            "right hand relaxed at side",
            "full hand visible",
            "clean space beside right hip",
        ],
        negative_additions=[
            "walking blur",
            "twisted fingers",
            "hidden hand",
            "purse",
            "bag",
        ],
        notes=["Use when walking poses produce poor hands or occlusion."],
    ),
)


def get_prompt_variants() -> list[HeroPromptVariant]:
    return list(PROMPT_VARIANTS)


def get_prompt_variant(variant_id: str) -> HeroPromptVariant | None:
    return next((variant for variant in PROMPT_VARIANTS if variant.variant_id == variant_id), None)


def resolve_prompt_variant(variant_id: str | None) -> HeroPromptVariant:
    selected = variant_id or "strict_empty_hand_no_accessory_v1"
    variant = get_prompt_variant(selected)
    if variant is None:
        raise ValueError(f"Unknown hero prompt variant: {selected}")
    return variant
