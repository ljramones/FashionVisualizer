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

| profile | model | device | status | duration | width | height | steps | guidance_scale | prompt_profile_used | supports_negative_prompt | output | fallback used | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sdxl_turbo_preview | stabilityai/sdxl-turbo | mps | success_real_generation | 4.661s | 512 | 768 | 2 | 0.0 | sdxl_turbo_preview | False | assets/outputs/model_probe/sdxl_turbo_preview/8cd895924b6cbff4/hero_still.png | False | See docs/model_probe_results.md for full notes. |
| sdxl_base_quality | stabilityai/stable-diffusion-xl-base-1.0 | mps | success_real_generation | 19.045s | 512 | 768 | 20 | 6.0 | sdxl_base_quality | True | assets/outputs/model_probe/sdxl_base_quality/8cd895924b6cbff4/hero_still.png | False | See docs/model_probe_results.md for full notes. |
| flux_schnell_quality_gated | black-forest-labs/FLUX.1-schnell | mps | fallback_gated_model_access | 0.819s | 512 | 768 | 4 | 0.0 | flux_schnell_quality_gated | False | assets/outputs/model_probe/flux_schnell_quality_gated/8cd895924b6cbff4/hero_still.png | True | 401 Client Error. (Request ID: Root=1-6a0d05d4-1626494e6cf738536a7fa8dc;d216d890-cdd6-4be9-9bd8-1361be952556) |
