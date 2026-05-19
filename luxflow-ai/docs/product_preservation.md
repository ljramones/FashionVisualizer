# Product Preservation

The handbag should not be hallucinated by diffusion. The source product is the commercial object, so its silhouette, material, logo area, straps, hardware, and proportions must remain recognizable.

Product-locked compositing means the generative model should create context and motion around the product while the product itself is protected by masks and overlays. The freeze mask concept identifies pixels or regions that should survive destructive diffusion.

Future implementation should:

- Generate or ingest a product mask.
- Composite the source handbag into the hero still.
- Restrict edits around high-risk areas such as logos and straps.
- Compare generated output against the source image for similarity.
- Project or track the locked product region through video frames.

The current code documents this policy but does not perform image analysis.
