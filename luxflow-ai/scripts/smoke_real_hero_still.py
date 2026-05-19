import json

from backend.app import config
from backend.app.config import project_root
from backend.app.demo import load_golden_generation_request
from backend.app.pipeline.handbag_pipeline import run_handbag_pipeline
from backend.app.recipes.scene_recipe_compiler import compile_scene_recipe


def main() -> None:
    print("Optional real hero-still smoke test")
    print("This may download model weights and may require model access approval.")
    print("Install optional dependencies first: pip install -e \".[dev,generation]\"")
    config.settings.enable_real_image_generation = True

    recipe = compile_scene_recipe(load_golden_generation_request())
    entry = run_handbag_pipeline(recipe)
    output_dir = project_root() / "assets/outputs" / entry.recipe_hash
    trace = json.loads((output_dir / "pipeline_trace.json").read_text(encoding="utf-8"))
    hero_generation = trace["hero_still_generation"]

    print(f"request_hash: {entry.recipe_hash}")
    print(f"hero_still: {next(a.path for a in entry.artifacts if a.kind == 'hero_still')}")
    print(f"pipeline_trace: {next(a.path for a in entry.artifacts if a.kind == 'pipeline_trace')}")
    print(f"model_id: {hero_generation['model_id']}")
    print(f"device: {hero_generation['device']}")
    print(f"used_real_generation: {hero_generation['used_real_generation']}")
    print(f"fallback_used: {hero_generation['fallback_used']}")


if __name__ == "__main__":
    main()
