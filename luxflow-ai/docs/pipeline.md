# Pipeline

The current handbag pipeline creates real local files for a compiled recipe. The hero-still stage can optionally use Diffusers; all other stages remain deterministic placeholders.

Planned stages:

1. Hero still generation from the compiled scene recipe.
2. Product-locked composite using source product imagery and masks.
3. LTX or equivalent image-to-video route.
4. Ping-pong loop export for catalog browsing.
5. Evaluation of prompt adherence and product preservation.
6. Catalog publishing to local metadata.

Current status:

- Recipe compilation is implemented.
- Route selection is implemented as a deterministic stub.
- `POST /generate` writes artifacts under `assets/outputs/{request_hash}/`.
- `POST /demo/run-golden` runs the canonical golden recipe.
- `hero_still.png` is generated with Pillow by default, or with optional Diffusers when enabled and available.
- `product_locked_composite.png` and `thumbnail.png` are generated with Pillow.
- `final_video_placeholder.json` is written instead of a real video.
- `catalog_entry.json` and `pipeline_trace.json` record the artifact lifecycle.
- `pipeline_trace.json` records hero-still generation timing, dependency status, selected device, fallback status, and error summary.
- Product lock functions return policy metadata only.
- Evaluation uses honest placeholder scores; prompt adherence is not measured.

No ComfyUI workflow or video route is executed. Optional Diffusers hero-still execution is disabled by default and falls back cleanly to the placeholder renderer.

## Real Hero-Still Validation

The default Diffusers model is `black-forest-labs/FLUX.1-schnell`. In the current validation pass, optional dependencies installed and the route attempted a real hero still, but Hugging Face returned gated model access (`401`). The pipeline did not fail the request; it rendered the placeholder hero still, continued product-lock composite and thumbnail creation, and persisted the failure reason in the trace.

## Image Model Probe

`scripts/probe_image_models.py` runs the same golden recipe through configured candidate models. Each candidate still uses `run_handbag_pipeline`, so any successful real hero still flows through the same artifact store, product-lock placeholder, thumbnail creation, evaluation placeholder, catalog entry, and pipeline trace.

The current probe produced real hero stills with SDXL Turbo and SDXL base. The normal golden demo path was also verified with SDXL Turbo, so `assets/outputs/{request_hash}/hero_still.png` can now be a real Diffusers image while the product-locked composite, thumbnail, video placeholder, evaluation, and catalog entry remain unchanged.
