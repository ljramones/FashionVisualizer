from pathlib import Path

from backend.app.config import settings
from backend.app.contracts import ArtifactRef, CatalogEntry, EvalResult, SceneRecipe
from backend.app.eval.metrics import evaluate_catalog_entry
from backend.app.generation.diffusers_hero_still import (
    GenerationResult,
    generate_hero_still_with_diffusers,
    resolve_device,
)
from backend.app.pipeline.artifact_store import ArtifactStore
from backend.app.pipeline.placeholder_render import (
    render_hero_still_placeholder,
    render_product_locked_composite_placeholder,
    render_thumbnail,
)
from backend.app.pipeline.product_lock import build_product_freeze_policy
from backend.app.publisher.catalog_publisher import publish_catalog_entry
from backend.app.routing.model_router import choose_route


def _artifact_ref(store: ArtifactStore, kind: str, path: Path, mime_type: str) -> ArtifactRef:
    return ArtifactRef(
        kind=kind,
        path=store.relative_path(path),
        static_url=store.static_url(path),
        mime_type=mime_type,
        exists=path.exists(),
    )


def _render_hero_still(recipe: SceneRecipe, hero_path: Path) -> tuple[Path, dict[str, object], str]:
    device = resolve_device()
    metadata: dict[str, object] = {
        "backend_requested": settings.image_generation_backend,
        "real_generation_enabled": settings.enable_real_image_generation,
        "used_real_generation": False,
        "model_id": settings.image_model_id,
        "device": device,
        "fallback_used": True,
        "notes": [],
    }

    if not settings.enable_real_image_generation:
        render_hero_still_placeholder(recipe, hero_path)
        metadata["notes"] = ["Real image generation disabled; rendered placeholder hero still."]
        return hero_path, metadata, "Hero still placeholder rendered"

    if settings.image_generation_backend != "diffusers":
        render_hero_still_placeholder(recipe, hero_path)
        metadata["notes"] = [
            f"Unsupported image generation backend: {settings.image_generation_backend}.",
            "Rendered placeholder hero still.",
        ]
        return hero_path, metadata, "Hero still placeholder rendered"

    result: GenerationResult = generate_hero_still_with_diffusers(recipe, hero_path)
    metadata.update(
        {
            "used_real_generation": result.success,
            "model_id": result.model_id,
            "device": result.device,
            "fallback_used": not result.success,
            "notes": result.notes,
            "error": result.error,
        }
    )

    if result.success and result.output_path is not None:
        return result.output_path, metadata, "Real hero still generated with Diffusers"

    render_hero_still_placeholder(recipe, hero_path)
    return hero_path, metadata, "Hero still placeholder rendered"


def run_handbag_pipeline(recipe: SceneRecipe, output_root: Path | None = None) -> CatalogEntry:
    """Run a deterministic placeholder artifact pipeline without invoking ML models."""

    route = choose_route(recipe)
    store = ArtifactStore(recipe.request_hash, output_root=output_root)
    freeze_policy = build_product_freeze_policy(recipe.product)

    hero_path, hero_generation_metadata, hero_stage_label = _render_hero_still(
        recipe,
        store.path_for("hero_still.png"),
    )
    composite_path = render_product_locked_composite_placeholder(
        recipe,
        store.path_for("product_locked_composite.png"),
    )
    thumbnail_path = render_thumbnail(composite_path, store.path_for("thumbnail.png"))
    video_placeholder_path = store.write_json(
        "final_video_placeholder.json",
        {
            "request_hash": recipe.request_hash,
            "route": route.model_dump(mode="json"),
            "artifact_type": "video_placeholder",
            "note": "No real video was generated. Future LTX or equivalent route writes here.",
        },
    )
    catalog_entry_path = store.path_for("catalog_entry.json")
    trace_path = store.path_for("pipeline_trace.json")

    entry = CatalogEntry(
        id=f"placeholder_{recipe.request_hash}",
        product=recipe.product,
        model=recipe.model,
        location=recipe.location,
        action=recipe.action,
        recipe_hash=recipe.request_hash,
        route=route,
        artifacts=[
            _artifact_ref(store, "hero_still", hero_path, "image/png"),
            _artifact_ref(store, "product_locked_composite", composite_path, "image/png"),
            _artifact_ref(store, "thumbnail", thumbnail_path, "image/png"),
            _artifact_ref(store, "video_placeholder", video_placeholder_path, "application/json"),
            ArtifactRef(
                kind="catalog_entry",
                path=store.relative_path(catalog_entry_path),
                static_url=store.static_url(catalog_entry_path),
                mime_type="application/json",
                exists=False,
            ),
            ArtifactRef(
                kind="pipeline_trace",
                path=store.relative_path(trace_path),
                static_url=store.static_url(trace_path),
                mime_type="application/json",
                exists=False,
            ),
        ],
        eval=EvalResult(notes=["Evaluation pending pipeline placeholder completion."]),
        status="stub",
    )
    entry.eval = evaluate_catalog_entry(entry)
    store.write_json("catalog_entry.json", entry)

    trace = {
        "request_hash": recipe.request_hash,
        "route": route.name,
        "route_detail": route.model_dump(mode="json"),
        "mode": recipe.mode.value,
        "ml_execution": bool(hero_generation_metadata["used_real_generation"]),
        "hero_still_generation": hero_generation_metadata,
        "product_preservation": freeze_policy,
        "stages": [
            {
                "stage_id": "recipe_compiled",
                "label": "Scene recipe compiled",
                "status": "completed",
                "notes": ["Resolved product, model, location, and action metadata."],
            },
            {
                "stage_id": "hero_still_placeholder_rendered",
                "label": hero_stage_label,
                "status": "completed",
                "notes": hero_generation_metadata["notes"],
            },
            {
                "stage_id": "product_locked_composite_placeholder_rendered",
                "label": "Product-locked composite placeholder rendered",
                "status": "completed",
                "notes": ["Product lock layer is represented visually and in metadata."],
            },
            {
                "stage_id": "thumbnail_rendered",
                "label": "Thumbnail rendered",
                "status": "completed",
                "notes": ["Thumbnail derived from the product-locked composite."],
            },
            {
                "stage_id": "video_placeholder_written",
                "label": "Video placeholder metadata written",
                "status": "completed",
                "notes": ["No playable video was produced in this pass."],
            },
            {
                "stage_id": "eval_completed",
                "label": "Placeholder evaluation completed",
                "status": "completed",
                "notes": ["Prompt adherence remains unmeasured without a vision model."],
            },
            {
                "stage_id": "catalog_entry_written",
                "label": "Catalog entry metadata written",
                "status": "completed",
                "notes": ["Catalog entry JSON records all local artifact references."],
            },
        ],
        "next_real_stage": (
            "Replace hero_still placeholder renderer with local image-generation route"
        ),
    }
    store.write_json("pipeline_trace.json", trace)
    for artifact in entry.artifacts:
        if artifact.kind in {"catalog_entry", "pipeline_trace"}:
            artifact.exists = True
    store.write_json("catalog_entry.json", entry)
    return publish_catalog_entry(entry)
