from pydantic import BaseModel, Field


class ImageModelCandidate(BaseModel):
    id: str
    display_name: str
    purpose: str
    expected_steps: int
    default_width: int
    default_height: int
    guidance_scale: float
    license_note: str
    access_note: str
    smoke_test_priority: int = Field(ge=1)


MODEL_CANDIDATES: tuple[ImageModelCandidate, ...] = (
    ImageModelCandidate(
        id="black-forest-labs/FLUX.1-schnell",
        display_name="FLUX.1 schnell",
        purpose="Aspirational quality route for fast preview stills.",
        expected_steps=4,
        default_width=512,
        default_height=512,
        guidance_scale=0.0,
        license_note="Apache-2.0 per model card; verify current terms before production use.",
        access_note="May require Hugging Face access approval and login.",
        smoke_test_priority=1,
    ),
    ImageModelCandidate(
        id="stabilityai/sdxl-turbo",
        display_name="SDXL Turbo",
        purpose="Fast local smoke-test route for proving one real Diffusers still.",
        expected_steps=2,
        default_width=512,
        default_height=512,
        guidance_scale=0.0,
        license_note=(
            "sai-nc-community style terms; use as a development smoke test unless "
            "the license fits the intended use."
        ),
        access_note="May require license review or Hugging Face authentication.",
        smoke_test_priority=2,
    ),
    ImageModelCandidate(
        id="stabilityai/stable-diffusion-xl-base-1.0",
        display_name="SDXL base 1.0",
        purpose="Reference text-to-image fallback for accessible local validation.",
        expected_steps=20,
        default_width=768,
        default_height=768,
        guidance_scale=6.0,
        license_note="CreativeML Open RAIL++ style terms; verify current model card.",
        access_note="May require license acceptance depending on Hugging Face account state.",
        smoke_test_priority=3,
    ),
)


def get_model_candidates() -> list[ImageModelCandidate]:
    return sorted(MODEL_CANDIDATES, key=lambda candidate: candidate.smoke_test_priority)


def get_model_candidate(model_id: str) -> ImageModelCandidate | None:
    return next((candidate for candidate in MODEL_CANDIDATES if candidate.id == model_id), None)
