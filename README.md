# FashionVisualizer

FashionVisualizer is the parent repository for the LuxFlow AI architecture project. The active implementation lives in [`luxflow-ai/`](luxflow-ai/), a local-first workflow studio for product-preserving generative catalog videos.

## Current Project

[`luxflow-ai/`](luxflow-ai/) demonstrates a staged AI workflow for luxury handbag catalog media:

- declarative scene recipes
- FastAPI backend and Pydantic contracts
- React/Vite workflow UI
- deterministic local artifact lifecycle
- product-lock placeholder pipeline
- golden recipe demo
- optional Diffusers hero-still route with safe fallback

Start with the project README:

- [LuxFlow AI README](luxflow-ai/README.md)
- [Current Status](luxflow-ai/docs/current_status.md)
- [Architecture](luxflow-ai/docs/architecture.md)
- [Pipeline](luxflow-ai/docs/pipeline.md)
- [Local Execution](luxflow-ai/docs/local_execution.md)
- [Tech Stack](luxflow-ai/docs/tech_stack.md)
- [Product Preservation](luxflow-ai/docs/product_preservation.md)
- [Model Access](luxflow-ai/docs/model_access.md)
- [Model Probe Results](luxflow-ai/docs/model_probe_results.md)
- [Benchmark Results](luxflow-ai/docs/benchmark_results.md)
- [Roadmap](luxflow-ai/docs/roadmap.md)

## Quick Start

```bash
cd luxflow-ai
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
make test
make lint
make demo
```

Run the backend:

```bash
cd luxflow-ai
make backend
```

Run the frontend:

```bash
cd luxflow-ai/frontend
npm install
npm run dev
```

## Optional Real Hero-Still Route

The project installs without heavy ML dependencies by default. To try the optional Diffusers hero-still route:

```bash
cd luxflow-ai
pip install -e ".[dev,generation]"
LUXFLOW_ENABLE_REAL_IMAGE_GENERATION=true python scripts/smoke_real_hero_still.py
```

The default model may require Hugging Face access approval and authentication. If generation is unavailable, the pipeline falls back to deterministic placeholder artifacts and records the reason in `pipeline_trace.json`.

## Repository Notes

- Generated artifacts under `luxflow-ai/assets/outputs/` are ignored except `.gitkeep`.
- Model weights, caches, credentials, and local environment files should not be committed.
- Contributor guidance is in [AGENTS.md](AGENTS.md).
