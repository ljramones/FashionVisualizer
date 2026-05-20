from backend.app.contracts import GenerationRequest
from backend.app.generation.prompt_profiles import build_hero_still_prompt
from backend.app.recipes.scene_recipe_compiler import compile_scene_recipe


def _recipe():
    return compile_scene_recipe(
        GenerationRequest(
            product_id="black_structured_bag",
            model_id="adult_female_editorial_01",
            location_id="hotel_lobby",
            action_id="walking_with_bag",
        )
    )


def test_prompt_includes_scene_context() -> None:
    bundle = build_hero_still_prompt(_recipe(), "sdxl_turbo_preview")

    assert "hotel_lobby" not in bundle.positive_prompt
    assert "hotel lobby" in bundle.positive_prompt.lower()
    assert "walking" in bundle.positive_prompt.lower()
    assert "female" in bundle.positive_prompt.lower()


def test_prompt_avoids_exact_product_generation() -> None:
    bundle = build_hero_still_prompt(
        _recipe(),
        "sdxl_turbo_preview",
        "editorial_empty_hand_v1",
    )
    prompt = bundle.positive_prompt.lower()

    assert "exact black structured handbag" not in prompt
    assert "right hand clear" in prompt
    assert "product composited later" in prompt
    assert "no prominent bag" in prompt
    assert "right hand" in prompt
    assert bundle.prompt_variant_id == "editorial_empty_hand_v1"
    assert "right_hand" in bundle.composition_target_summary


def test_negative_prompt_contains_product_preservation_terms() -> None:
    bundle = build_hero_still_prompt(_recipe(), "sdxl_base_quality")
    negative = bundle.negative_prompt.lower()

    for term in [
        "distorted bag",
        "warped product",
        "changed logo",
        "extra straps",
        "floating object",
        "broken hands",
        "deformed fingers",
        "flicker",
        "fake brand logo",
        "malformed handbag",
        "purse",
        "bag",
    ]:
        assert term in negative
