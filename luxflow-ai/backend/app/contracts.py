from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field


class ProductCategory(StrEnum):
    handbag = "handbag"


class GenerationMode(StrEnum):
    cached = "cached"
    preview = "preview"
    quality = "quality"


AspectRatio = Literal["1:1", "9:16"]
GenderPresentation = Literal["male", "female", "neutral"]
ModelSource = Literal["synthetic", "licensed_reference", "anonymous"]
LoopPolicy = Literal["ping_pong", "none"]
ProductAnchorTarget = Literal["right_hand", "left_hand", "shoulder", "right_hip", "left_hip"]
CompositeLayerOrder = Literal["foreground", "midground"]


class CompositeAnchor(BaseModel):
    anchor_id: str
    x_ratio: float = Field(ge=0.0, le=1.0)
    y_ratio: float = Field(ge=0.0, le=1.0)
    scale_ratio: float = Field(gt=0.0, le=1.0)
    rotation_degrees: float = 0.0
    layer_order: CompositeLayerOrder = "foreground"
    notes: list[str] = Field(default_factory=list)


class ProductRef(BaseModel):
    id: str
    name: str
    category: ProductCategory
    description: str
    image_path: str | None = None
    mask_path: str | None = None
    preservation_notes: str


class ModelProfile(BaseModel):
    id: str
    display_name: str
    gender_presentation: GenderPresentation
    source: ModelSource
    provenance_note: str


class LocationRef(BaseModel):
    id: str
    name: str
    prompt_fragment: str
    lighting: str
    mood: str


class ActionRef(BaseModel):
    id: str
    name: str
    prompt_fragment: str
    camera_motion: str
    product_interaction: str
    loop_policy: LoopPolicy
    product_anchor_target: ProductAnchorTarget | None = None
    composition_space_hint: str | None = None
    occlusion_hint: str | None = None
    hero_action_prompt_fragment: str | None = None
    hero_pose_intent: str | None = None
    final_catalog_action_label: str | None = None
    forbidden_generated_objects: list[str] = Field(default_factory=list)
    composite_anchor: CompositeAnchor | None = None


class GenerationRequest(BaseModel):
    product_id: str
    model_id: str
    location_id: str
    action_id: str
    seed: int = Field(default=42, ge=0)
    aspect_ratio: AspectRatio = "9:16"
    mode: GenerationMode = GenerationMode.preview


class SceneRecipe(BaseModel):
    product: ProductRef
    model: ModelProfile
    location: LocationRef
    action: ActionRef
    compiled_prompt: str
    negative_prompt: str
    route_hint: str
    request_hash: str
    seed: int
    aspect_ratio: AspectRatio
    mode: GenerationMode


class PipelineRoute(BaseModel):
    name: str
    engine: str
    mode: GenerationMode
    available: bool = False
    reason: str


class ArtifactRef(BaseModel):
    kind: str
    path: str
    static_url: str | None = None
    mime_type: str | None = None
    exists: bool = False


class EvalResult(BaseModel):
    prompt_adherence_score: float | None = None
    product_preservation_score: float | None = None
    notes: list[str] = Field(default_factory=list)


class CatalogEntry(BaseModel):
    id: str
    product: ProductRef
    model: ModelProfile
    location: LocationRef
    action: ActionRef
    recipe_hash: str
    route: PipelineRoute
    artifacts: list[ArtifactRef]
    eval: EvalResult
    status: Literal["cached", "stub", "complete"] = "stub"


class SystemCapabilities(BaseModel):
    local_generation_available: bool = False
    diffusers_route_available: bool = False
    comfyui_route_available: bool = False
    ltx_video_route_available: bool = False
    mode_support: list[GenerationMode] = Field(
        default_factory=lambda: [
            GenerationMode.cached,
            GenerationMode.preview,
            GenerationMode.quality,
        ]
    )
