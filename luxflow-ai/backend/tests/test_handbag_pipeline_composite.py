import json

from backend.app.config import settings
from backend.app.contracts import GenerationRequest
from backend.app.pipeline.handbag_pipeline import run_handbag_pipeline
from backend.app.recipes.scene_recipe_compiler import compile_scene_recipe
from PIL import Image


def test_handbag_pipeline_writes_real_product_composite_trace(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(settings, "enable_real_image_generation", False)
    recipe = compile_scene_recipe(
        GenerationRequest(
            product_id="black_structured_bag",
            model_id="adult_female_editorial_01",
            location_id="hotel_lobby",
            action_id="standing_right_hand_visible",
        )
    )

    first = run_handbag_pipeline(recipe, output_root=tmp_path)
    second = run_handbag_pipeline(recipe, output_root=tmp_path)
    output_dir = tmp_path / recipe.request_hash
    composite_path = output_dir / "product_locked_composite.png"
    thumbnail_path = output_dir / "thumbnail.png"
    trace = json.loads((output_dir / "pipeline_trace.json").read_text(encoding="utf-8"))

    assert first.recipe_hash == second.recipe_hash
    assert composite_path.exists()
    assert thumbnail_path.exists()
    with Image.open(output_dir / "hero_still.png") as hero:
        with Image.open(composite_path) as composite:
            assert composite.size == hero.size
    assert trace["product_locked_composite"]["used_real_composite"] is True
    assert trace["product_locked_composite"]["composite_method"] == (
        "manual_anchor_alpha_overlay_v1"
    )
    assert trace["product_locked_composite"]["anchor_id"] == "right_hand_side_v2"
    assert trace["product_locked_composite"]["product_has_alpha"] is True
    assert trace["product_locked_composite"]["product_alpha_bbox"] is not None
    assert trace["product_locked_composite"]["default_anchor_used"] is True
    assert trace["product_locked_composite"]["anchor_override_used"] is False
    assert trace["product_locked_composite"]["freeze_core_pixels"] is True
    assert trace["product_locked_composite"]["destructive_diffusion_allowed"] is False
    assert any(
        stage["stage_id"] == "product_locked_composite_rendered"
        for stage in trace["stages"]
    )
