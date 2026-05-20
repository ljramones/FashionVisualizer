# Golden Demo Recipe

`golden_recipe.json` is the canonical local demo request for LuxFlow AI. It keeps
the original catalog intent: a model eventually shown with a handbag.

`golden_empty_hand_recipe.json` is the preferred hero-still generation request
for product-compositing prep. It uses an empty-hand action so the image model
creates the adult model, scene, and pose without hallucinating a bag-like object.

It exercises the current deterministic placeholder artifact pipeline:

- compile a public `GenerationRequest` into a `SceneRecipe`
- choose the preview handbag route
- write local artifacts under `assets/outputs/{request_hash}/`
- produce hero still, product-locked composite, thumbnail, trace, and catalog metadata

This demo does not run ML, download model weights, call hosted APIs, or produce a real video.
When real image generation is enabled, the empty-hand recipe is the safer default
for creating a scene canvas before product-locked compositing.
