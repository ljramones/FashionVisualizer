from typing import Literal

from pydantic import BaseModel, Field

AspectRatioName = Literal["1:1", "9:16"]


class ImageGenerationProfile(BaseModel):
    profile_id: str
    model_id: str
    purpose: str
    default_steps: int = Field(gt=0)
    default_guidance_scale: float = Field(ge=0)
    supports_negative_prompt: bool
    preferred_aspect_ratios: list[AspectRatioName]
    license_note: str
    access_note: str
    prompt_style_note: str


IMAGE_GENERATION_PROFILES: tuple[ImageGenerationProfile, ...] = (
    ImageGenerationProfile(
        profile_id="sdxl_turbo_preview",
        model_id="stabilityai/sdxl-turbo",
        purpose="Fast local preview route for real hero-still smoke tests.",
        default_steps=2,
        default_guidance_scale=0.0,
        supports_negative_prompt=False,
        preferred_aspect_ratios=["1:1", "9:16"],
        license_note=(
            "SDXL Turbo has more restrictive community/non-commercial style terms; "
            "treat as a local development smoke-test option unless the license fits."
        ),
        access_note="May require Hugging Face license review or authentication.",
        prompt_style_note="Short, direct prompts work best; avoid long recipe dumps.",
    ),
    ImageGenerationProfile(
        profile_id="sdxl_base_quality",
        model_id="stabilityai/stable-diffusion-xl-base-1.0",
        purpose="Slower reference route for higher-quality local hero stills.",
        default_steps=20,
        default_guidance_scale=6.0,
        supports_negative_prompt=True,
        preferred_aspect_ratios=["1:1", "9:16"],
        license_note="CreativeML Open RAIL++ style terms; verify current model card.",
        access_note="May require license acceptance depending on Hugging Face account state.",
        prompt_style_note="Supports more descriptive prompts and negative prompting.",
    ),
    ImageGenerationProfile(
        profile_id="flux_schnell_quality_gated",
        model_id="black-forest-labs/FLUX.1-schnell",
        purpose="Aspirational high-quality fast route once model access is available.",
        default_steps=4,
        default_guidance_scale=0.0,
        supports_negative_prompt=False,
        preferred_aspect_ratios=["1:1", "9:16"],
        license_note="Apache-2.0 per model card; verify current terms before production use.",
        access_note="May require Hugging Face access approval and login.",
        prompt_style_note="Use concise product-empty scene prompts; access is gated.",
    ),
)


def get_image_profiles() -> list[ImageGenerationProfile]:
    return list(IMAGE_GENERATION_PROFILES)


def get_image_profile(profile_id: str) -> ImageGenerationProfile | None:
    return next(
        (profile for profile in IMAGE_GENERATION_PROFILES if profile.profile_id == profile_id),
        None,
    )


def get_profile_for_model(model_id: str) -> ImageGenerationProfile:
    return next(
        (
            profile
            for profile in IMAGE_GENERATION_PROFILES
            if profile.model_id == model_id
        ),
        IMAGE_GENERATION_PROFILES[2],
    )


def resolve_image_profile(profile_id: str | None, model_id: str) -> ImageGenerationProfile:
    if profile_id:
        profile = get_image_profile(profile_id)
        if profile is None:
            raise ValueError(f"Unknown image generation profile: {profile_id}")
        return profile
    return get_profile_for_model(model_id)
