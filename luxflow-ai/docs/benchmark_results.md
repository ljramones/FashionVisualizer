# Placeholder Benchmark Results

This artifact starts with planned route comparisons and then records local smoke-test results. It does not call hosted APIs, commit model weights, or claim production quality.

| route | purpose | expected strength | expected limitation | implementation status |
| --- | --- | --- | --- | --- |
| diffusers_reference | Optional preview hero still generation | Readable local Python route with placeholder fallback | Requires optional dependencies and model access for real generation | Optional |
| comfyui_visual_stub | Visual workflow orchestration for quality route | Inspectable node graph and staged outputs | ComfyUI is not installed or executed | Stub |
| ltx_video_stub | Future local image-to-video route | Motion generation from product-locked stills | No video model installed | Placeholder |

## Real Hero-Still Validation

This manual validation row records the first optional Diffusers route attempt. The route fell back cleanly; no generated media is committed.

| route | model | device | status | duration | output type | notes |
| --- | --- | --- | --- | --- | --- | --- |
| handbag_diffusers_reference | black-forest-labs/FLUX.1-schnell | mps | fallback_model_access_required | 0.858s | placeholder PNG | Hugging Face returned gated model access (401); pipeline trace captured the fallback. |

## Image Model Probe Results

| model | device | status | duration | output | fallback used | notes |
| --- | --- | --- | --- | --- | --- | --- |
| black-forest-labs/FLUX.1-schnell | mps | fallback_gated_model_access | 0.800s | assets/outputs/model_probe/black-forest-labs__FLUX.1-schnell/8cd895924b6cbff4/hero_still.png | True | 401 Client Error. (Request ID: Root=1-6a0cff29-17f82a6335ec60485a83c335;54d4a3c7-99b5-4026-bc7c-e556d90bc0a5) |
| stabilityai/sdxl-turbo | mps | success_real_generation | 4.391s | assets/outputs/model_probe/stabilityai__sdxl-turbo/8cd895924b6cbff4/hero_still.png | False | See docs/model_probe_results.md for full notes. |
| stabilityai/stable-diffusion-xl-base-1.0 | mps | success_real_generation | 28.186s | assets/outputs/model_probe/stabilityai__stable-diffusion-xl-base-1.0/8cd895924b6cbff4/hero_still.png | False | See docs/model_probe_results.md for full notes. |
