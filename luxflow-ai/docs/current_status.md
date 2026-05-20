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
- product-locked composite placeholder
- thumbnail rendering
- static artifact serving
- golden recipe demo
- optional Diffusers hero-still route
- graceful placeholder fallback when generation is disabled or unavailable
- pipeline trace timing, dependency status, and fallback/error reporting
- image model candidate metadata and probe script
- confirmed real hero-still generation with SDXL Turbo and SDXL base

## Not Yet Implemented

- ComfyUI route execution
- LTX route execution
- real video export
- real CLIP evaluation
- product tracking/projection
- hosted fallback

The project currently demonstrates request-to-artifact workflow architecture. Real image generation is optional, disabled by default, and limited to the hero-still stage.

## Real Hero-Still Validation

Optional generation dependencies installed successfully in this pass: `torch 2.12.0`, `diffusers 0.38.0`, and `transformers 5.8.1`. The unrestricted smoke run selected Apple `mps` and attempted `black-forest-labs/FLUX.1-schnell`.

The model did not generate an image because Hugging Face returned gated model access (`401`). The pipeline fell back cleanly to the deterministic placeholder renderer and recorded dependency status, device, duration, fallback status, and the error summary in `pipeline_trace.json`.

## Image Model Probe

`scripts/probe_image_models.py` tests configured Diffusers candidates against the golden recipe and writes `docs/model_probe_results.md`. The first candidate remains FLUX.1-schnell as the quality target, with SDXL Turbo and SDXL base available as lower-friction smoke-test alternatives.

Observed probe result: FLUX.1-schnell fell back due to gated model access, SDXL Turbo generated a real 512x512 hero still on `mps`, and SDXL base generated a real 768x768 hero still on `mps`.
