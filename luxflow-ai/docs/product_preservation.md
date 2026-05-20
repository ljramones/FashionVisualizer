# Product Preservation

The handbag should not be hallucinated by diffusion. The source product is the commercial object, so its silhouette, material, logo area, straps, hardware, and proportions must remain recognizable.

Product-locked compositing means the generative model should create context and motion around the product while the product itself is protected by masks and overlays. The freeze mask concept identifies pixels or regions that should survive destructive diffusion.

Current implementation:

- Loads the product image from `ProductRef.image_path`.
- Uses deterministic transparent `product_alpha.png` demo assets for handbag products.
- Places the product onto `hero_still.png` with manual action-level anchor presets.
- Writes `product_locked_composite.png`.
- Records alpha status, placement, anchor selection, and freeze metadata in `pipeline_trace.json`.
- Allows deterministic resize/rotation for placement only.
- Does not run diffusion, relighting, segmentation, background removal, or image-to-image edits over the product layer.

Future implementation should:

- Ingest real product cutouts or product masks.
- Restrict edits around high-risk areas such as logos and straps.
- Add simple shadows or edge blending without changing product core pixels.
- Compare generated output against the source image for similarity.
- Project or track the locked product region through video frames.

The current freeze policy:

- `freeze_core_pixels: true`
- `preserve_alpha_layer: true`
- `allow_resize: true`
- `allow_rotation: true`
- `allow_edge_feathering: false`
- `allow_contact_shadow: false`
- `destructive_diffusion_allowed: false`

This is not image analysis and does not prove product similarity. It proves the architectural rule: the product is a controlled layer, not an object invented by the image model.

## Manual Anchor Tuning

Placement is intentionally manual in this POC. The `standing_right_hand_visible` action stores several anchor presets so the same hero still can be reviewed with different x/y/scale settings. This avoids adding pose estimation before the static compositing problem is visually acceptable.

Current missing polish:

- contact shadows
- edge feathering
- occlusion handling
- relighting
- pose-based tracking
- video projection
