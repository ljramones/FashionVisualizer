# Product Preservation

The handbag should not be hallucinated by diffusion. The source product is the commercial object, so its silhouette, material, logo area, straps, hardware, and proportions must remain recognizable.

Product-locked compositing means the generative model should create context and motion around the product while the product itself is protected by masks and overlays. The freeze mask concept identifies pixels or regions that should survive destructive diffusion.

Future implementation should:

- Generate or ingest a product mask.
- Composite the source handbag into the hero still.
- Restrict edits around high-risk areas such as logos and straps.
- Compare generated output against the source image for similarity.
- Project or track the locked product region through video frames.

The current implementation writes a product-locked composite placeholder with a marked handbag layer and a freeze policy:

- `freeze_core_pixels: true`
- `allow_edge_feathering: true`
- `allow_contact_shadow: true`
- `destructive_diffusion_allowed: false`

This is not image analysis and does not prove product similarity. It establishes the metadata and artifact lifecycle needed before destructive generation stages are introduced.
