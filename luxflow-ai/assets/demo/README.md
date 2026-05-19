# Golden Demo Recipe

`golden_recipe.json` is the canonical local demo request for LuxFlow AI.

It exercises the current deterministic placeholder artifact pipeline:

- compile a public `GenerationRequest` into a `SceneRecipe`
- choose the preview handbag route
- write local artifacts under `assets/outputs/{request_hash}/`
- produce hero still, product-locked composite, thumbnail, trace, and catalog metadata

This demo does not run ML, download model weights, call hosted APIs, or produce a real video.
It is intended to become the first real hero-still route in a later implementation pass.
