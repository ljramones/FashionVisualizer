# Architecture

LuxFlow AI is a workflow studio, not a generator. The first implementation pass focuses on contracts, routing, metadata, and inspection so the generation engines can be added later without reshaping the application.

```mermaid
flowchart LR
  A[React/Vite App] --> B[FastAPI Backend]
  B --> C[Registry]
  C --> D[Scene Recipe Compiler]
  D --> E[Router]
  E --> F[Pipeline]
  F --> G[Product Lock Layer]
  G --> H[Video Export]
  H --> I[Eval]
  I --> J[Catalog Publisher]
```

The React app has two modes. Catalog mode reads curated placeholder entries. Workflow mode lets a user select product, model, location, action, mode, and aspect ratio, then compile a deterministic `SceneRecipe` or request a stub catalog entry.

The FastAPI backend owns the public API, Pydantic contracts, and local registry access. The registry reads JSON metadata from `assets/`. The compiler resolves IDs into typed objects, builds prompts, and creates deterministic request hashes for future caching.

The router chooses planned execution routes: cached catalog, Diffusers reference stub, ComfyUI visual stub, or unsupported. No route currently executes models. The pipeline layer returns placeholder artifacts and evaluation notes while documenting the future stages: hero still, product-locked composite, image-to-video, ping-pong export, evaluation, and publishing.

Product preservation is a first-class boundary. Future generation should use masks, compositing, and similarity checks so diffusion enhances the scene without replacing or hallucinating the handbag.
