# Benchmarking

Benchmarking currently compares planned routes, not real model performance. This keeps the architecture honest while avoiding fake speed or quality claims before model execution exists.

| route | purpose | expected strength | expected limitation | implementation status |
| --- | --- | --- | --- | --- |
| diffusers_reference | Optional preview hero still generation | Readable local Python route with placeholder fallback | Requires optional dependencies and model access for real generation | Optional |
| comfyui_visual_stub | Visual workflow orchestration for quality route | Inspectable node graph and staged outputs | ComfyUI is not installed or executed | Stub |
| ltx_video_stub | Future local image-to-video route | Motion generation from product-locked stills | No video model installed | Placeholder |

Future benchmarks should record runtime, VRAM/RAM use, output dimensions, prompt adherence, product preservation, and failure modes.

## Real Hero-Still Validation

The optional Diffusers route was attempted with `black-forest-labs/FLUX.1-schnell`. Optional dependencies installed, but Hugging Face returned gated model access (`401`), so the route fell back to the placeholder renderer. See `docs/benchmark_results.md` for the recorded validation row.

## Image Model Probe

Run `python scripts/probe_image_models.py` to test configured candidates against the golden recipe. The probe writes `docs/model_probe_results.md` and a JSON copy under ignored `assets/outputs/`.

Current result: SDXL Turbo and SDXL base generated real hero stills on `mps`; FLUX.1-schnell fell back due to gated model access.
