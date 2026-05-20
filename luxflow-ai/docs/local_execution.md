# Local Execution

LuxFlow AI is local-first. The backend reads local metadata, compiles local recipes, and returns local placeholder artifact paths. Hosted fallback is only a future route placeholder.

Modes:

- `cached`: read curated catalog metadata and avoid generation.
- `preview`: Diffusers reference route with optional real hero-still generation and placeholder fallback.
- `quality`: future higher-control route, currently mapped to a ComfyUI visual stub.

Apple Silicon/MPS can be used by optional PyTorch installs when available. ComfyUI and LTX are future execution routes. They are not installed, started, or invoked in this repository pass.

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

Optional real hero-still generation:

```bash
pip install -e ".[dev,generation]"
LUXFLOW_ENABLE_REAL_IMAGE_GENERATION=true python scripts/run_golden_demo.py
```

The first real run may download model weights and may require accepting model access terms. The generated hero still does not attempt to generate the exact handbag; product fidelity remains handled by the product-lock/composite stage.

Real hero-still validation command:

```bash
LUXFLOW_ENABLE_REAL_IMAGE_GENERATION=true python scripts/smoke_real_hero_still.py
```

Observed result for the default model in this pass: dependencies installed, Apple `mps` was selected in an unrestricted run, and `black-forest-labs/FLUX.1-schnell` fell back because Hugging Face returned gated model access (`401`). The fallback still produced local artifacts and wrote timing, device, dependency status, and the error summary to `pipeline_trace.json`.

Probe configured image models:

```bash
python scripts/probe_image_models.py
```

Observed local probe result: `stabilityai/sdxl-turbo` and `stabilityai/stable-diffusion-xl-base-1.0` produced real hero stills on Apple `mps`. FLUX.1-schnell still requires Hugging Face gated model access.

Run a specific candidate without editing `.env`:

```bash
python scripts/run_golden_demo.py \
  --real-image \
  --profile-id sdxl_turbo_preview \
  --width 512 \
  --height 768 \
  --steps 2 \
  --guidance-scale 0.0 \
  --device auto
```

## Hero-Still Prompt Strategy

The real hero still is a product-empty scene base. It should generate the adult model, location, walking/standing action, lighting, mood, and catalog framing. It should not generate the exact handbag. The prompt leaves natural hand placement and empty space near one hand so the later product-locked composite can insert the real product layer.

## Aspect Ratio Handling

`1:1` and `9:16` are supported at the public contract level. The Diffusers route resolves concrete dimensions per image profile and mode. Preview defaults stay small for local iteration, such as `512x512` for square and `512x768` for portrait. Explicit CLI dimensions are accepted when both width and height are provided and both are multiples of 8.

Run frontend:

```bash
cd frontend
npm install
npm run dev
```

The frontend reads `VITE_API_BASE_URL`; see `frontend/.env.example`.
