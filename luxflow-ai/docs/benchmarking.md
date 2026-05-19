# Benchmarking

Benchmarking currently compares planned routes, not real model performance. This keeps the architecture honest while avoiding fake speed or quality claims before model execution exists.

| route | purpose | expected strength | expected limitation | implementation status |
| --- | --- | --- | --- | --- |
| diffusers_reference_stub | Preview handbag hero stills and fast iteration | Simple local reference path | No real generation or product lock yet | Stub |
| comfyui_visual_stub | Visual workflow orchestration for quality route | Inspectable node graph and staged outputs | ComfyUI is not installed or executed | Stub |
| ltx_video_stub | Future local image-to-video route | Motion generation from product-locked stills | No video model installed | Placeholder |

Future benchmarks should record runtime, VRAM/RAM use, output dimensions, prompt adherence, product preservation, and failure modes.
