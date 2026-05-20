# Tech Stack

- React, Vite, and TypeScript provide the workflow studio UI.
- FastAPI exposes local HTTP endpoints and generated OpenAPI docs.
- Pydantic defines stable public contracts between UI, backend, and future engines.
- SQLite and local JSON metadata are the intended early persistence layer.
- Diffusers reference route is implemented as an optional hero-still path.
- ComfyUI visual route is reserved for inspectable staged workflows.
- LTX video route placeholder represents future local image-to-video execution.
- MoviePy or ffmpeg are deferred for future ping-pong video export.

Heavy ML dependencies are optional. `torch`, `diffusers`, `transformers`, and `accelerate` live behind the `generation` extra and are not required for normal install, tests, or placeholder demos. OpenCV and MoviePy are still deferred.

## Real Hero-Still Validation

`pip install -e ".[dev,generation]"` installed the optional generation stack in this pass:

- `torch 2.12.0`
- `diffusers 0.38.0`
- `transformers 5.8.1`

The default model remains configurable through `LUXFLOW_IMAGE_MODEL_ID`. The attempted default, `black-forest-labs/FLUX.1-schnell`, returned gated model access (`401`) during validation, so the route fell back to the Pillow placeholder. Users may retry after accepting model access/authenticating with Hugging Face or set a smaller smoke-test model ID without changing the artifact lifecycle.

## Image Model Probe

`backend/app/generation/model_candidates.py` lists candidate Diffusers models with access and license notes. `scripts/probe_image_models.py` tests those candidates without adding another generation path. The current candidates are FLUX.1-schnell, SDXL Turbo, and SDXL base.

Observed local result: SDXL Turbo and SDXL base generated real hero stills on Apple `mps` after forcing float32 loading for CPU/MPS smoke runs. FLUX.1-schnell remains configured as an aspirational model but requires gated Hugging Face access.
