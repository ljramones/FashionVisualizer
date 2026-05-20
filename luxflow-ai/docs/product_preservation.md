# Product Preservation

The handbag should not be hallucinated by diffusion. The source product is the commercial object, so its silhouette, material, logo area, straps, hardware, and proportions must remain recognizable.

Product-locked compositing means the generative model should create context and motion around the product while the product itself is protected by masks and overlays. The freeze mask concept identifies pixels or regions that should survive destructive diffusion.

Current implementation:

- Loads the product image from `ProductRef.image_path`.
- Places it onto `hero_still.png` with a manual action-level `composite_anchor`.
- Writes `product_locked_composite.png`.
- Records placement and freeze metadata in `pipeline_trace.json`.
- Allows deterministic resize/rotation for placement only.
- Does not run diffusion, relighting, segmentation, background removal, or image-to-image edits over the product layer.

Future implementation should:

- Generate or ingest a product mask.
- Composite the source handbag into the hero still.
- Restrict edits around high-risk areas such as logos and straps.
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
