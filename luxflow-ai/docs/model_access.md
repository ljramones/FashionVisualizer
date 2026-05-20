# Model Access

LuxFlow AI keeps image generation optional. The default install does not download model weights, and generated outputs under `assets/outputs/` are ignored by Git.

## Candidate Models

| model | role | access note | license note |
| --- | --- | --- | --- |
| `black-forest-labs/FLUX.1-schnell` | Aspirational quality target | May require Hugging Face access approval and login | Apache-2.0 per model card; verify current terms |
| `stabilityai/sdxl-turbo` | Fast smoke-test candidate | May require license review or authentication | More restrictive community/non-commercial style terms; use only if appropriate |
| `stabilityai/stable-diffusion-xl-base-1.0` | Reference fallback candidate | May require license acceptance depending on account state | CreativeML Open RAIL++ style terms; verify current terms |

## Hugging Face Login

If a model requires authentication, log in locally without writing tokens into this repository:

```bash
huggingface-cli login
```

Do not commit tokens, `.env` files, model caches, or generated PNGs.

## Change Model

Use environment variables:

```bash
LUXFLOW_ENABLE_REAL_IMAGE_GENERATION=true \
LUXFLOW_IMAGE_MODEL_ID=stabilityai/sdxl-turbo \
LUXFLOW_IMAGE_WIDTH=512 \
LUXFLOW_IMAGE_HEIGHT=512 \
LUXFLOW_IMAGE_STEPS=2 \
LUXFLOW_IMAGE_GUIDANCE_SCALE=0.0 \
python scripts/run_golden_demo.py
```

Or use CLI overrides:

```bash
python scripts/run_golden_demo.py \
  --real-image \
  --model-id stabilityai/sdxl-turbo \
  --width 512 \
  --height 512 \
  --steps 2 \
  --guidance-scale 0.0
```

## Probe Models

Run:

```bash
pip install -e ".[dev,generation]"
python scripts/probe_image_models.py
```

The probe attempts each configured candidate against the golden recipe, records success/failure/fallback behavior, and writes `docs/model_probe_results.md`. It also writes a JSON copy under `assets/outputs/model_probe_results.json`, which remains ignored.

Current observed result: FLUX.1-schnell requires gated Hugging Face access, while SDXL Turbo and SDXL base generated real hero stills locally on Apple `mps`.
