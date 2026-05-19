# Pipeline

The current handbag pipeline is a deterministic placeholder artifact pipeline. It creates real local files for a compiled recipe while still avoiding model execution.

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
- `hero_still.png`, `product_locked_composite.png`, and `thumbnail.png` are generated with Pillow.
- `final_video_placeholder.json` is written instead of a real video.
- `catalog_entry.json` and `pipeline_trace.json` record the artifact lifecycle.
- Product lock functions return policy metadata only.
- Evaluation uses honest placeholder scores; prompt adherence is not measured.

No ML model, ComfyUI workflow, or video route is executed.
