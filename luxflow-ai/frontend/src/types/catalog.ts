export type GenerationMode = "cached" | "preview" | "quality";
export type AspectRatio = "1:1" | "9:16";

export interface CatalogSampleEntry {
  id: string;
  product_name: string;
  model: string;
  location: string;
  action: string;
  route: string;
  video_path: string;
  eval_notes: string[];
}

export interface CatalogResponse {
  entries: CatalogSampleEntry[];
}

export interface ProductRef {
  id: string;
  name: string;
  category: "handbag";
  description: string;
  image_path?: string | null;
  mask_path?: string | null;
  preservation_notes: string;
}

export interface ModelProfile {
  id: string;
  display_name: string;
  gender_presentation: "male" | "female" | "neutral";
  source: "synthetic" | "licensed_reference" | "anonymous";
  provenance_note: string;
}

export interface LocationRef {
  id: string;
  name: string;
  prompt_fragment: string;
  lighting: string;
  mood: string;
}

export interface ActionRef {
  id: string;
  name: string;
  prompt_fragment: string;
  camera_motion: string;
  product_interaction: string;
  loop_policy: "ping_pong" | "none";
}

export interface GenerationRequest {
  product_id: string;
  model_id: string;
  location_id: string;
  action_id: string;
  seed: number;
  aspect_ratio: AspectRatio;
  mode: GenerationMode;
}

export interface PipelineTrace {
  request_hash: string;
  route: string;
  mode: GenerationMode;
  ml_execution: boolean;
  stages: {
    stage_id: string;
    label: string;
    status: string;
    notes: string[];
  }[];
  product_preservation: {
    freeze_core_pixels: boolean;
    destructive_diffusion_allowed: boolean;
    notes: string[];
  };
  hero_still_generation: {
    backend_requested: string;
    real_generation_enabled: boolean;
    generation_attempted: boolean;
    used_real_generation: boolean;
    model_id: string;
    device: string;
    profile_id?: string | null;
    width?: number | null;
    height?: number | null;
    steps?: number | null;
    guidance_scale?: number | null;
    supports_negative_prompt?: boolean | null;
    positive_prompt_preview?: string | null;
    negative_prompt_preview?: string | null;
    aspect_ratio_requested?: string | null;
    aspect_ratio_resolved?: string | null;
    prompt_strategy?: string | null;
    prompt_profile_used?: string | null;
    dependency_status: {
      torch_available: boolean;
      diffusers_available: boolean;
      torch_version: string | null;
      diffusers_version: string | null;
      mps_available: boolean;
      cuda_available: boolean;
    };
    fallback_used: boolean;
    notes: string[];
    started_at?: string | null;
    completed_at?: string | null;
    duration_seconds?: number | null;
    error_summary?: string | null;
    error?: string | null;
  };
  next_real_stage: string;
}

export interface PipelineRoute {
  name: string;
  engine: string;
  mode: GenerationMode;
  available: boolean;
  reason: string;
}

export interface EvalResult {
  prompt_adherence_score: number | null;
  product_preservation_score: number | null;
  notes: string[];
}

export interface SceneRecipe {
  product: ProductRef;
  model: ModelProfile;
  location: LocationRef;
  action: ActionRef;
  compiled_prompt: string;
  negative_prompt: string;
  route_hint: string;
  request_hash: string;
  seed: number;
  aspect_ratio: AspectRatio;
  mode: GenerationMode;
}

export interface CatalogEntry {
  id: string;
  product: ProductRef;
  model: ModelProfile;
  location: LocationRef;
  action: ActionRef;
  recipe_hash: string;
  route: PipelineRoute;
  artifacts: {
    kind: string;
    path: string;
    static_url?: string | null;
    mime_type?: string | null;
    exists: boolean;
  }[];
  eval: EvalResult;
  status: "cached" | "stub" | "complete";
}
