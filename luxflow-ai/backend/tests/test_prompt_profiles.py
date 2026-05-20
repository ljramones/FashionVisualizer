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


def _empty_hand_recipe():
    return compile_scene_recipe(
        GenerationRequest(
            product_id="black_structured_bag",
            model_id="adult_female_editorial_01",
            location_id="hotel_lobby",
            action_id="standing_right_hand_visible",
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
        _empty_hand_recipe(),
        "sdxl_turbo_preview",
        "strict_empty_hand_no_accessory_v1",
    )
    prompt = bundle.positive_prompt.lower()

    assert "exact black structured handbag" not in prompt
    assert "handbag" not in prompt
    assert " purse" not in f" {prompt}"
    assert " tote" not in f" {prompt}"
    assert " clutch" not in f" {prompt}"
    assert "clear placement area" in prompt
    assert "clear placement" in prompt
    assert "right hand" in prompt
    assert bundle.prompt_variant_id == "strict_empty_hand_no_accessory_v1"
    assert bundle.final_catalog_action_label == "standing with handbag"
    assert "right_hip" in bundle.composition_target_summary
    assert bundle.no_accessory_strategy is True


def test_negative_prompt_contains_product_preservation_terms() -> None:
    bundle = build_hero_still_prompt(_empty_hand_recipe(), "sdxl_base_quality")
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
        "tote",
        "clutch",
        "backpack",
        "branded accessory",
    ]:
        assert term in negative


def test_prompt_builder_prefers_hero_action_prompt_fragment() -> None:
    recipe = _empty_hand_recipe()
    bundle = build_hero_still_prompt(recipe, "sdxl_turbo_preview")

    assert recipe.action.prompt_fragment.lower() not in bundle.positive_prompt.lower()
    assert recipe.action.hero_action_prompt_fragment is not None
    assert recipe.action.hero_action_prompt_fragment in bundle.positive_prompt
    assert bundle.hero_action_prompt_used == recipe.action.hero_action_prompt_fragment
