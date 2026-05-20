import argparse
import json

from backend.app import config
from backend.app.config import project_root
from backend.app.contracts import CatalogEntry
from backend.app.demo import load_golden_generation_request
from backend.app.pipeline.handbag_pipeline import run_handbag_pipeline
from backend.app.recipes.scene_recipe_compiler import compile_scene_recipe
from backend.app.routing.model_router import choose_route


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the LuxFlow AI golden recipe demo.")
    parser.add_argument("--real-image", action="store_true", help="Enable real image generation.")
    parser.add_argument("--profile-id", help="Use a named image generation profile.")
    parser.add_argument("--model-id", help="Override LUXFLOW_IMAGE_MODEL_ID for this run.")
    parser.add_argument("--width", type=int, help="Override generated image width.")
    parser.add_argument("--height", type=int, help="Override generated image height.")
    parser.add_argument("--steps", type=int, help="Override image inference steps.")
    parser.add_argument("--guidance-scale", type=float, help="Override image guidance scale.")
    parser.add_argument(
        "--device",
        choices=["auto", "mps", "cpu", "cuda"],
        help="Override generation device selection.",
    )
    return parser.parse_args()


def apply_cli_overrides(args: argparse.Namespace) -> None:
    if args.real_image:
        config.settings.enable_real_image_generation = True
    if args.profile_id is not None:
        config.settings.image_profile_id = args.profile_id
    if args.model_id is not None:
        config.settings.image_model_id = args.model_id
    if args.width is not None:
        config.settings.image_width = args.width
    if args.height is not None:
        config.settings.image_height = args.height
    if args.steps is not None:
        config.settings.image_steps = args.steps
    if args.guidance_scale is not None:
        config.settings.image_guidance_scale = args.guidance_scale
    if args.device is not None:
        config.settings.image_device = args.device


def run_golden_demo() -> CatalogEntry:
    request = load_golden_generation_request()
    recipe = compile_scene_recipe(request)
    choose_route(recipe)
    return run_handbag_pipeline(recipe)


def _artifact_path(entry: CatalogEntry, kind: str) -> str:
    for artifact in entry.artifacts:
        if artifact.kind == kind:
            return artifact.path
    return "missing"


def main() -> None:
    apply_cli_overrides(parse_args())

    entry = run_golden_demo()
    output_dir = project_root() / "assets/outputs" / entry.recipe_hash
    trace = json.loads((output_dir / "pipeline_trace.json").read_text(encoding="utf-8"))
    hero_generation = trace.get("hero_still_generation", {})

    print("LuxFlow AI golden demo complete")
    print(f"request_hash: {entry.recipe_hash}")
    print(f"output_directory: {output_dir.relative_to(project_root()).as_posix()}")
    print(f"hero_still: {_artifact_path(entry, 'hero_still')}")
    print(f"product_composite: {_artifact_path(entry, 'product_locked_composite')}")
    print(f"thumbnail: {_artifact_path(entry, 'thumbnail')}")
    print(f"catalog_entry: {_artifact_path(entry, 'catalog_entry')}")
    print(f"pipeline_trace: {_artifact_path(entry, 'pipeline_trace')}")
    print(f"real_image_generation_enabled: {hero_generation.get('real_generation_enabled')}")
    print(f"used_real_generation: {hero_generation.get('used_real_generation')}")
    print(f"model_id: {hero_generation.get('model_id')}")
    print(f"profile_id: {hero_generation.get('profile_id')}")
    print(f"device: {hero_generation.get('device')}")
    print(f"width: {hero_generation.get('width')}")
    print(f"height: {hero_generation.get('height')}")
    print(f"steps: {hero_generation.get('steps')}")
    print(f"guidance_scale: {hero_generation.get('guidance_scale')}")
    print(f"generation_attempted: {hero_generation.get('generation_attempted')}")
    print(f"fallback_used: {hero_generation.get('fallback_used')}")
    print(f"duration_seconds: {hero_generation.get('duration_seconds')}")
    if hero_generation.get("error_summary"):
        print(f"error_summary: {hero_generation.get('error_summary')}")


if __name__ == "__main__":
    main()
