from backend.app.contracts import GenerationRequest
from backend.app.recipes.scene_recipe_compiler import compile_scene_recipe, request_hash


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


def test_request_hash_changes_when_public_request_fields_change() -> None:
    base = GenerationRequest(
        product_id="black_structured_bag",
        model_id="adult_female_editorial_01",
        location_id="hotel_lobby",
        action_id="walking_with_bag",
        seed=42,
        aspect_ratio="9:16",
        mode="preview",
    )

    variants = [
        base.model_copy(update={"product_id": "tan_travel_tote"}),
        base.model_copy(update={"model_id": "adult_male_editorial_01"}),
        base.model_copy(update={"location_id": "modern_gallery"}),
        base.model_copy(update={"action_id": "standing_turn_with_bag"}),
        base.model_copy(update={"seed": 43}),
        base.model_copy(update={"aspect_ratio": "1:1"}),
        base.model_copy(update={"mode": "quality"}),
    ]

    base_hash = request_hash(base)
    assert all(request_hash(variant) != base_hash for variant in variants)


def test_negative_prompt_contains_product_preservation_terms() -> None:
    recipe = compile_scene_recipe(
        GenerationRequest(
            product_id="black_structured_bag",
            model_id="adult_female_editorial_01",
            location_id="hotel_lobby",
            action_id="walking_with_bag",
        )
    )

    for term in [
        "distorted bag",
        "warped product",
        "changed logo",
        "extra straps",
        "floating object",
        "broken hands",
        "flicker",
    ]:
        assert term in recipe.negative_prompt
