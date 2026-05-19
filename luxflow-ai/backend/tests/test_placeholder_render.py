from backend.app.contracts import GenerationRequest
from backend.app.pipeline.placeholder_render import (
    render_hero_still_placeholder,
    render_product_locked_composite_placeholder,
    render_thumbnail,
)
from backend.app.recipes.scene_recipe_compiler import compile_scene_recipe
from PIL import Image


def test_placeholder_render_creates_valid_pngs(tmp_path) -> None:
    recipe = compile_scene_recipe(
        GenerationRequest(
            product_id="black_structured_bag",
            model_id="adult_female_editorial_01",
            location_id="hotel_lobby",
            action_id="walking_with_bag",
        )
    )
    hero_path = tmp_path / "hero_still.png"
    composite_path = tmp_path / "product_locked_composite.png"
    thumbnail_path = tmp_path / "thumbnail.png"

    render_hero_still_placeholder(recipe, hero_path)
    render_product_locked_composite_placeholder(recipe, composite_path)
    render_thumbnail(composite_path, thumbnail_path)

    assert Image.open(hero_path).format == "PNG"
    assert Image.open(hero_path).size == (1024, 1024)
    assert Image.open(composite_path).format == "PNG"
    assert Image.open(thumbnail_path).size == (512, 512)
