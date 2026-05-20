from backend.app.contracts import ActionRef, GenerationMode, GenerationRequest
from backend.app.recipes.scene_recipe_compiler import request_hash


def test_generation_request_validates_sample_request() -> None:
    request = GenerationRequest(
        product_id="black_structured_bag",
        model_id="adult_female_editorial_01",
        location_id="hotel_lobby",
        action_id="walking_with_bag",
        seed=42,
        aspect_ratio="9:16",
        mode=GenerationMode.preview,
    )

    assert request.product_id == "black_structured_bag"
    assert request.mode == GenerationMode.preview


def test_request_hash_is_deterministic() -> None:
    first = GenerationRequest(
        product_id="black_structured_bag",
        model_id="adult_female_editorial_01",
        location_id="hotel_lobby",
        action_id="walking_with_bag",
        seed=42,
        aspect_ratio="9:16",
        mode="preview",
    )
    second = GenerationRequest(**first.model_dump())

    assert request_hash(first) == request_hash(second)
    assert len(request_hash(first)) == 16


def test_action_ref_accepts_hero_stage_fields() -> None:
    action = ActionRef(
        id="standing_right_hand_visible",
        name="Standing Right Hand Visible",
        prompt_fragment="Final catalog action includes the product.",
        camera_motion="locked camera",
        product_interaction="product composited later",
        loop_policy="ping_pong",
        product_anchor_target="right_hip",
        hero_action_prompt_fragment="empty hands visible with clean right side placement space",
        hero_pose_intent="visible relaxed right hand",
        final_catalog_action_label="standing with handbag",
        forbidden_generated_objects=["handbag", "bag", "purse"],
    )

    assert action.hero_action_prompt_fragment is not None
    assert action.final_catalog_action_label == "standing with handbag"
    assert "purse" in action.forbidden_generated_objects
