from pathlib import Path

from backend.app.contracts import ArtifactRef, CatalogEntry, EvalResult, SceneRecipe
from backend.app.eval.metrics import evaluate_catalog_entry
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


def run_handbag_pipeline(recipe: SceneRecipe, output_root: Path | None = None) -> CatalogEntry:
    """Run a deterministic placeholder artifact pipeline without invoking ML models."""

    route = choose_route(recipe)
    store = ArtifactStore(recipe.request_hash, output_root=output_root)
    freeze_policy = build_product_freeze_policy(recipe.product)

    hero_path = render_hero_still_placeholder(recipe, store.path_for("hero_still.png"))
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
        "route": route.model_dump(mode="json"),
        "product_freeze_policy": freeze_policy,
        "stages": [
            {"name": "recipe_compiled", "status": "complete"},
            {"name": "hero_still_placeholder_rendered", "status": "complete"},
            {"name": "product_locked_composite_placeholder_rendered", "status": "complete"},
            {"name": "thumbnail_rendered", "status": "complete"},
            {"name": "video_placeholder_written", "status": "complete"},
            {"name": "eval_completed", "status": "complete"},
            {"name": "catalog_entry_written", "status": "complete"},
        ],
        "note": "No ML model was run; artifacts are deterministic Pillow placeholders.",
    }
    store.write_json("pipeline_trace.json", trace)
    for artifact in entry.artifacts:
        if artifact.kind in {"catalog_entry", "pipeline_trace"}:
            artifact.exists = True
    store.write_json("catalog_entry.json", entry)
    return publish_catalog_entry(entry)
