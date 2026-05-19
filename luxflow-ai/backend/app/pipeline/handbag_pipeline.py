from backend.app.contracts import ArtifactRef, CatalogEntry, EvalResult, SceneRecipe
from backend.app.eval.metrics import evaluate_catalog_entry
from backend.app.pipeline.product_lock import build_product_freeze_policy
from backend.app.publisher.catalog_publisher import publish_catalog_entry
from backend.app.routing.model_router import choose_route


def run_handbag_pipeline(recipe: SceneRecipe) -> CatalogEntry:
    """Run a handbag pipeline stub without invoking ML models."""

    route = choose_route(recipe)
    build_product_freeze_policy(recipe.product)

    # Future stages:
    # 1. hero still generation
    # 2. product-locked composite
    # 3. LTX image-to-video
    # 4. ping-pong export
    # 5. evaluation
    # 6. catalog publishing
    slug = f"{recipe.product.id}_{recipe.location.id}_{recipe.action.id}_{recipe.request_hash}"
    entry = CatalogEntry(
        id=f"stub_{slug}",
        product=recipe.product,
        model=recipe.model,
        location=recipe.location,
        action=recipe.action,
        recipe_hash=recipe.request_hash,
        route=route,
        artifacts=[
            ArtifactRef(
                kind="video",
                path=f"assets/outputs/{slug}.mp4",
                mime_type="video/mp4",
                exists=False,
            ),
            ArtifactRef(
                kind="recipe",
                path=f"assets/outputs/{slug}.json",
                mime_type="application/json",
                exists=False,
            ),
        ],
        eval=EvalResult(notes=["Evaluation pending pipeline stub completion."]),
        status="stub",
    )
    entry.eval = evaluate_catalog_entry(entry)
    return publish_catalog_entry(entry)
