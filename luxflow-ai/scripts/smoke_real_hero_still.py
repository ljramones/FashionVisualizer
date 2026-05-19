import json
from time import perf_counter

from backend.app import config
from backend.app.config import project_root
from backend.app.demo import load_golden_generation_request
from backend.app.generation.diffusers_hero_still import generation_dependency_status
from backend.app.pipeline.handbag_pipeline import run_handbag_pipeline
from backend.app.recipes.scene_recipe_compiler import compile_scene_recipe


def main() -> None:
    config.settings.enable_real_image_generation = True
    started = perf_counter()

    recipe = compile_scene_recipe(load_golden_generation_request())
    entry = run_handbag_pipeline(recipe)
    duration = perf_counter() - started
    output_dir = project_root() / "assets/outputs" / entry.recipe_hash
    trace = json.loads((output_dir / "pipeline_trace.json").read_text(encoding="utf-8"))
    hero_generation = trace["hero_still_generation"]

    print("Real Hero-Still Smoke Test")
    print("This may download model weights and may require model access approval.")
    print(f"- model: {hero_generation['model_id']}")
    print(f"- device: {hero_generation['device']}")
    print(f"- dependencies: {generation_dependency_status()}")
    print(f"- generation enabled: {hero_generation['real_generation_enabled']}")
    print(f"- success: {hero_generation['used_real_generation']}")
    print(f"- fallback used: {hero_generation['fallback_used']}")
    print(f"- duration: {duration:.3f}s")
    print(f"- output: {next(a.path for a in entry.artifacts if a.kind == 'hero_still')}")
    print(f"- trace: {next(a.path for a in entry.artifacts if a.kind == 'pipeline_trace')}")
    if hero_generation.get("error_summary"):
        print(f"- error: {hero_generation['error_summary']}")


if __name__ == "__main__":
    main()
