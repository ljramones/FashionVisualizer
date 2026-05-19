# Local Execution

LuxFlow AI is local-first. The backend reads local metadata, compiles local recipes, and returns local placeholder artifact paths. Hosted fallback is only a future route placeholder.

Modes:

- `cached`: read curated catalog metadata and avoid generation.
- `preview`: future fast local route, currently mapped to a Diffusers reference stub.
- `quality`: future higher-control route, currently mapped to a ComfyUI visual stub.

Apple Silicon, MPS, ComfyUI, and LTX are future execution routes. They are not installed, started, or invoked in this repository pass.

Current local artifact flow:

- `POST /generate` writes to `assets/outputs/{request_hash}/` by default.
- Set `LUXFLOW_OUTPUT_ROOT` to redirect outputs for tests or experiments.
- Generated PNGs are served from `/static/assets/outputs/...` in local development.
- Video output is represented by `final_video_placeholder.json`, not a playable video.

Run backend:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
make backend
```

Run checks:

```bash
make test
make lint
python scripts/seed_sample_catalog.py
python scripts/benchmark_models.py
python scripts/generate_placeholder_assets.py
```

Run the golden demo:

```bash
python scripts/run_golden_demo.py
```

Run frontend:

```bash
cd frontend
npm install
npm run dev
```

The frontend reads `VITE_API_BASE_URL`; see `frontend/.env.example`.
