# Tech Stack

- React, Vite, and TypeScript provide the workflow studio UI.
- FastAPI exposes local HTTP endpoints and generated OpenAPI docs.
- Pydantic defines stable public contracts between UI, backend, and future engines.
- SQLite and local JSON metadata are the intended early persistence layer.
- Diffusers reference route is implemented as an optional hero-still path.
- ComfyUI visual route is reserved for inspectable staged workflows.
- LTX video route placeholder represents future local image-to-video execution.
- MoviePy or ffmpeg are deferred for future ping-pong video export.

Heavy ML dependencies are optional. `torch`, `diffusers`, `transformers`, and `accelerate` live behind the `generation` extra and are not required for normal install, tests, or placeholder demos. OpenCV and MoviePy are still deferred.
