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

## Not Yet Implemented

- authenticated successful FLUX generation in this local validation pass
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
