from backend.app.contracts import GenerationMode, GenerationRequest
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
