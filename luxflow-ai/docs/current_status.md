# Current Status

## Current Implemented

- FastAPI backend
- React/Vite frontend
- Pydantic contracts
- asset registry
- recipe compiler
- model router
- deterministic artifact store
- placeholder hero still rendering
- product-locked composite v1 with manual anchor alpha overlay
- thumbnail rendering
- static artifact serving
- golden recipe demo
- optional Diffusers hero-still route
- graceful placeholder fallback when generation is disabled or unavailable
- pipeline trace timing, dependency status, and fallback/error reporting
- image model candidate metadata and probe script
- confirmed real hero-still generation with SDXL Turbo and SDXL base
- image generation profiles for SDXL Turbo, SDXL base, and gated FLUX
- aspect-ratio-aware dimension resolver
- product-empty hero-still prompt profile
- prompt variants for product-empty composition targets
- prompt tuning contact-sheet script
- hero-stage action prompts separated from final catalog action labels
- empty-hand golden recipe for product-compositing prep
- product-lock trace metadata with placement coordinates and freeze policy
- deterministic transparent handbag demo assets
- manual composite anchor presets and anchor tuning contact-sheet script

## Not Yet Implemented

- pose-aware placement
- shadows, edge blending, and relighting
- ComfyUI route execution
- LTX route execution
- real video export
- real CLIP evaluation
- product tracking/projection
- hosted fallback

The project currently demonstrates request-to-artifact workflow architecture. Real image generation is optional, disabled by default, and limited to the hero-still stage.

## Product-Locked Composite v1

The pipeline now renders `product_locked_composite.png` by opening the hero still, loading the product layer from `product.image_path`, and placing it with action-level anchor metadata. Product pixels are controlled by the overlay layer. No diffusion, segmentation, relighting, or background removal is applied to the product.

`scripts/generate_product_alpha_assets.py` creates deterministic transparent `product_alpha.png` files for the demo handbags. These assets replace the rectangular placeholder problem while keeping the layer non-generative and non-branded.

`standing_right_hand_visible` now has multiple anchor presets with `right_hand_side_v2` as the default. `scripts/tune_composite_anchors.py` can render a contact sheet for manual comparison.

The trace records `manual_anchor_alpha_overlay_v1`, source path, alpha status, alpha bounding box, anchor ID, default/override usage, x/y/scale ratios, rendered size, rotation, `freeze_core_pixels: true`, and `destructive_diffusion_allowed: false`.

Still missing: shadows, edge feathering, occlusion, relighting, pose-based tracking, real product cutout ingestion, and video projection.

## Real Hero-Still Validation

Optional generation dependencies installed successfully in this pass: `torch 2.12.0`, `diffusers 0.38.0`, and `transformers 5.8.1`. The unrestricted smoke run selected Apple `mps` and attempted `black-forest-labs/FLUX.1-schnell`.

The model did not generate an image because Hugging Face returned gated model access (`401`). The pipeline fell back cleanly to the deterministic placeholder renderer and recorded dependency status, device, duration, fallback status, and the error summary in `pipeline_trace.json`.

## Image Model Probe

`scripts/probe_image_models.py` tests configured Diffusers candidates against the golden recipe and writes `docs/model_probe_results.md`. The first candidate remains FLUX.1-schnell as the quality target, with SDXL Turbo and SDXL base available as lower-friction smoke-test alternatives.

Observed probe result: FLUX.1-schnell fell back due to gated model access, while SDXL Turbo and SDXL base generated real `512x768` portrait hero stills on `mps`.

Updated prompt/aspect result: SDXL Turbo generated a real portrait `512x768` hero still through the normal golden demo path with `profile_id: sdxl_turbo_preview` and `used_real_generation: true`.

## Hero-Still Prompt Tuning

`scripts/tune_hero_prompts.py` generates variant/seed grids for manual review. The current variants focus on empty hand placement, side-carry composition space, and avoiding hallucinated bags or branded accessories. Tuning outputs are ignored; `docs/prompt_tuning_results.md` records the review table.

## Current Prompt Tuning Finding

Initial real prompt tuning produced valid Diffusers images but all reviewed outputs contained unwanted handbag or purse-like accessories. The issue is semantic leakage from the final catalog intent into the hero still. The current pass separates final catalog actions such as "walking with handbag" from hero-stage prompts such as "empty hands visible with clean placement space."

Latest review: standing empty-hand actions produce several no-obvious-accessory candidates, while slow-walk actions still tend to generate handbag-like objects. Product-lock refinement should use a standing candidate first, after manual confirmation of hand and placement usability.
