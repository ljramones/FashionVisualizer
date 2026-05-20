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
- `product_locked_composite.png` is a Pillow manual-anchor alpha overlay.
- `thumbnail.png` is generated from the product-locked composite.
- `final_video_placeholder.json` is written instead of a real video.
- `catalog_entry.json` and `pipeline_trace.json` record the artifact lifecycle.
- `pipeline_trace.json` records hero-still generation timing, dependency status, selected device, fallback status, and error summary.
- Product lock functions return explicit freeze policy metadata.
- Evaluation uses honest placeholder scores; prompt adherence is not measured.

No ComfyUI workflow or video route is executed. Optional Diffusers hero-still execution is disabled by default and falls back cleanly to the placeholder renderer.

## Real Hero-Still Validation

The default Diffusers model is `black-forest-labs/FLUX.1-schnell`. In the current validation pass, optional dependencies installed and the route attempted a real hero still, but Hugging Face returned gated model access (`401`). The pipeline did not fail the request; it rendered the placeholder hero still, continued product-lock composite and thumbnail creation, and persisted the failure reason in the trace.

## Image Model Probe

`scripts/probe_image_models.py` runs the same golden recipe through configured candidate models. Each candidate still uses `run_handbag_pipeline`, so any successful real hero still flows through the same artifact store, product-lock placeholder, thumbnail creation, evaluation placeholder, catalog entry, and pipeline trace.

The current probe produced real hero stills with SDXL Turbo and SDXL base. The normal golden demo path was also verified with SDXL Turbo, so `assets/outputs/{request_hash}/hero_still.png` can now be a real Diffusers image while the product-locked composite, thumbnail, video placeholder, evaluation, and catalog entry remain unchanged.

## Hero-Still Prompt Strategy

The hero-still route now builds a product-empty scene prompt. It asks for the adult editorial model, selected location, hero-stage action, lighting, mood, natural visible hands, and luxury catalog framing. It avoids asking for the final handbag or any similar accessory because the handbag is intended to be composited later through the product-lock layer.

Prompt variants add composition-specific pressure without changing the artifact lifecycle. Examples include `strict_empty_hand_no_accessory_v1`, `studio_safe_pose_v1`, and `minimal_accessory_free_v1`. Pipeline traces record the selected variant, final catalog action label, hero-stage action prompt, forbidden generated objects, and composition target summary.

## Hero Action vs Final Catalog Action

The final catalog action can remain product-facing, such as "walking with handbag." The hero-still generation action is deliberately product-empty, such as "empty hands visible, right hand relaxed near the right hip, clear placement space." The image model should generate a scene canvas, not the sellable handbag. Later product-locked compositing owns the product pixels.

Current empty-hand action assets:

- `standing_right_hand_visible`
- `slow_walk_right_hand_visible`

The older `walking_with_bag` action remains available for comparison but now also carries a safer `hero_action_prompt_fragment`.

## Hero-Still Prompt Tuning

`scripts/tune_hero_prompts.py` runs a small grid of prompt variants and seeds through the existing Diffusers hero-still route, then writes an ignored contact sheet and a tracked Markdown review table. Manual review is expected because the current pipeline has no vision-based quality scorer.

Current tuning finding: the first contact sheet technically succeeded but generated unwanted bag-like accessories. The current mitigation is stronger hero-action decoupling plus the `strict_empty_hand_no_accessory_v1` variant.

Latest tuning result: `standing_right_hand_visible` produces the best no-accessory candidates. `slow_walk_right_hand_visible` still frequently generates bag-like objects and should remain a comparison route until the action is simplified or a stronger prompt/profile is selected.

## Product-Locked Composite v1

The composite stage now uses `manual_anchor_alpha_overlay_v1`:

1. Open `hero_still.png`.
2. Load the transparent product image from `ProductRef.image_path`.
3. Resolve the requested, default, or fallback action anchor.
4. Resize and rotate the product layer deterministically.
5. Paste the product with alpha onto the hero still.
6. Write `product_locked_composite.png`.

If a product image is missing, the compositor creates a labeled deterministic fallback layer and records the fallback in trace notes. V1 does not perform pose estimation, segmentation, background removal, shadows, edge blending, relighting, or diffusion over product pixels.

The trace records product source path, alpha status, alpha bounding box, anchor ID, whether the default or an override anchor was used, x/y ratios, pixel placement, layer size, scale, rotation, freeze policy, and `destructive_diffusion_allowed: false`.

## Transparent Product Assets

`scripts/generate_product_alpha_assets.py` creates deterministic transparent PNG demo assets for the handbag products. These files are intentionally simple: silhouette, handle, color, and minor hardware detail with no logo or opaque rectangle. Real product photos can be used later if they already include an alpha channel or a prepared mask.

The current project does not use SAM, rembg, or any other background-removal model. Rectangular/no-alpha assets are still accepted, but the loader records that they do not provide useful transparency.

## Manual Anchor Tuning

Manual anchors are stored in action metadata so placement remains data-driven. `standing_right_hand_visible` includes several right-hand/right-hip presets, and `default_composite_anchor_id` selects the current default.

Use the tuning helper to compare anchors against the same hero still:

```bash
python scripts/tune_composite_anchors.py \
  --output-dir assets/outputs/<request_hash> \
  --anchors right_hand_side_v1 right_hand_side_v2 right_hip_mid_v1 right_hip_lower_v1
```

The script writes ignored composites/contact sheets under `assets/outputs/composite_anchor_tuning/` and updates `docs/composite_anchor_tuning_results.md` for manual review.

## Why Not Video Yet?

Video remains deferred because product placement needs to work on a still first. Once the manual anchor and product layer are visually acceptable, the project can evaluate anchor presets, simple compositing polish, and only then product projection or image-to-video routes.

## Aspect Ratio Handling

The route resolves requested aspect ratio into model-friendly dimensions through image profiles. The golden `9:16` request can now produce a portrait `512x768` SDXL Turbo image instead of a square smoke output. Larger quality sizes remain profile-specific and should be benchmarked before becoming defaults.
