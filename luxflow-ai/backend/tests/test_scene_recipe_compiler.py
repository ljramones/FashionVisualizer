from backend.app.contracts import GenerationRequest
from backend.app.recipes.scene_recipe_compiler import compile_scene_recipe


def test_scene_recipe_compiler_returns_expected_prompt_fragments() -> None:
    recipe = compile_scene_recipe(
        GenerationRequest(
            product_id="black_structured_bag",
            model_id="adult_female_editorial_01",
            location_id="hotel_lobby",
            action_id="walking_with_bag",
            seed=42,
            aspect_ratio="9:16",
            mode="preview",
        )
    )

    assert recipe.product.name == "Black Structured Bag"
    assert "refined hotel lobby" in recipe.compiled_prompt
    assert "walks slowly" in recipe.compiled_prompt
    assert "distorted bag" in recipe.negative_prompt
    assert recipe.route_hint == "handbag:preview"
