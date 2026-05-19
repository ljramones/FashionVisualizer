# Pipeline

The current handbag pipeline is a stub that returns a mock `CatalogEntry`. It exists to lock down interfaces before model execution is introduced.

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
- Artifact paths are placeholders.
- Product lock functions return policy metadata only.
- Video export returns the planned output path and does not call ffmpeg.
- Evaluation scores are `None` until real media exists.
