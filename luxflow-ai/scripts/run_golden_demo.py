from backend.app.config import project_root
from backend.app.contracts import CatalogEntry
from backend.app.demo import load_golden_generation_request
from backend.app.pipeline.handbag_pipeline import run_handbag_pipeline
from backend.app.recipes.scene_recipe_compiler import compile_scene_recipe
from backend.app.routing.model_router import choose_route


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
    entry = run_golden_demo()
    output_dir = project_root() / "assets/outputs" / entry.recipe_hash

    print("LuxFlow AI golden demo complete")
    print(f"request_hash: {entry.recipe_hash}")
    print(f"output_directory: {output_dir.relative_to(project_root()).as_posix()}")
    print(f"hero_still: {_artifact_path(entry, 'hero_still')}")
    print(f"product_composite: {_artifact_path(entry, 'product_locked_composite')}")
    print(f"thumbnail: {_artifact_path(entry, 'thumbnail')}")
    print(f"catalog_entry: {_artifact_path(entry, 'catalog_entry')}")
    print(f"pipeline_trace: {_artifact_path(entry, 'pipeline_trace')}")


if __name__ == "__main__":
    main()
