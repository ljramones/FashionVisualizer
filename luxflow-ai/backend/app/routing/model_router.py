from backend.app.contracts import GenerationMode, PipelineRoute, ProductCategory, SceneRecipe


def choose_route(recipe: SceneRecipe) -> PipelineRoute:
    if recipe.mode == GenerationMode.cached:
        return PipelineRoute(
            name="cached_catalog",
            engine="local_cache",
            mode=recipe.mode,
            available=False,
            reason="Cached mode uses existing catalog metadata and placeholder artifacts.",
        )

    if recipe.product.category == ProductCategory.handbag and recipe.mode == GenerationMode.preview:
        return PipelineRoute(
            name="handbag_diffusers_reference_stub",
            engine="diffusers_reference_stub",
            mode=recipe.mode,
            available=False,
            reason="Preview route reserved for a future lightweight Diffusers reference path.",
        )

    if recipe.product.category == ProductCategory.handbag and recipe.mode == GenerationMode.quality:
        return PipelineRoute(
            name="handbag_comfyui_visual_stub",
            engine="comfyui_visual_stub",
            mode=recipe.mode,
            available=False,
            reason="Quality route reserved for a future ComfyUI visual workflow path.",
        )

    return PipelineRoute(
        name="unsupported_stub",
        engine="none",
        mode=recipe.mode,
        available=False,
        reason="No implemented route exists for this request.",
    )
