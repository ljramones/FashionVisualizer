# Tech Stack

- React, Vite, and TypeScript provide the workflow studio UI.
- FastAPI exposes local HTTP endpoints and generated OpenAPI docs.
- Pydantic defines stable public contracts between UI, backend, and future engines.
- SQLite and local JSON metadata are the intended early persistence layer.
- Diffusers reference route is reserved for a lightweight local preview path.
- ComfyUI visual route is reserved for inspectable staged workflows.
- LTX video route placeholder represents future local image-to-video execution.
- MoviePy or ffmpeg are deferred for future ping-pong video export.

Heavy ML dependencies are intentionally deferred. `torch`, `diffusers`, `transformers`, OpenCV, and MoviePy are not required dependencies because this pass does not execute models. Optional extras document likely future installation targets without forcing large downloads.
