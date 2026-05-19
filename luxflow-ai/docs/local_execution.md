# Local Execution

LuxFlow AI is local-first. The backend reads local metadata, compiles local recipes, and returns local placeholder artifact paths. Hosted fallback is only a future route placeholder.

Modes:

- `cached`: read curated catalog metadata and avoid generation.
- `preview`: future fast local route, currently mapped to a Diffusers reference stub.
- `quality`: future higher-control route, currently mapped to a ComfyUI visual stub.

Apple Silicon, MPS, ComfyUI, and LTX are future execution routes. They are not installed, started, or invoked in this repository pass.

Run backend:

```bash
make backend
```

Run frontend:

```bash
make frontend
```
