from backend.app.contracts import GenerationRequest
from backend.app.recipes.scene_recipe_compiler import compile_scene_recipe
from backend.app.routing.model_router import choose_route


def _recipe_for_mode(mode: str):
    return compile_scene_recipe(
        GenerationRequest(
            product_id="black_structured_bag",
            model_id="adult_female_editorial_01",
            location_id="hotel_lobby",
            action_id="walking_with_bag",
            seed=42,
            aspect_ratio="9:16",
            mode=mode,
        )
    )


def test_router_chooses_cached_route() -> None:
    route = choose_route(_recipe_for_mode("cached"))
    assert route.name == "cached_catalog"


def test_router_chooses_preview_route() -> None:
    route = choose_route(_recipe_for_mode("preview"))
    assert route.name == "handbag_diffusers_reference_stub"


def test_router_chooses_quality_route() -> None:
    route = choose_route(_recipe_for_mode("quality"))
    assert route.name == "handbag_comfyui_visual_stub"
