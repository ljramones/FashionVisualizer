from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS_PATH = ROOT / "docs/benchmark_results.md"

ROWS = [
    (
        "diffusers_reference",
        "Optional preview hero still generation",
        "Readable local Python route with placeholder fallback",
        "Requires optional dependencies and model access for real generation",
        "Optional",
    ),
    (
        "comfyui_visual_stub",
        "Visual workflow orchestration for quality route",
        "Inspectable node graph and staged outputs",
        "ComfyUI is not installed or executed",
        "Stub",
    ),
    (
        "ltx_video_stub",
        "Future local image-to-video route",
        "Motion generation from product-locked stills",
        "No video model installed",
        "Placeholder",
    ),
]


def render_table() -> str:
    lines = [
        "# Placeholder Benchmark Results",
        "",
        "This artifact compares planned routes only. It does not execute real models, "
        "download weights, call hosted APIs, or measure runtime quality yet.",
        "",
        "| route | purpose | expected strength | expected limitation | implementation status |",
        "| --- | --- | --- | --- | --- |",
    ]
    lines.extend(
        f"| {route} | {purpose} | {strength} | {limitation} | {status} |"
        for route, purpose, strength, limitation, status in ROWS
    )
    lines.extend(
        [
            "",
            "## Real Hero-Still Validation",
            "",
            "This manual validation row records the first optional Diffusers route attempt. "
            "The route fell back cleanly; no generated media is committed.",
            "",
            "| route | model | device | status | duration | output type | notes |",
            "| --- | --- | --- | --- | --- | --- | --- |",
            "| handbag_diffusers_reference | black-forest-labs/FLUX.1-schnell | mps | "
            "fallback_model_access_required | 0.858s | placeholder PNG | Hugging Face "
            "returned gated model access (401); pipeline trace captured the fallback. |",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    RESULTS_PATH.write_text(render_table(), encoding="utf-8")
    print(f"Wrote {RESULTS_PATH}")


if __name__ == "__main__":
    main()
