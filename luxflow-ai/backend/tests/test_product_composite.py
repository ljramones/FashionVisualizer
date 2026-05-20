from pathlib import Path

from backend.app.contracts import ActionRef, CompositeAnchor, ProductRef
from backend.app.pipeline.product_composite import (
    render_product_locked_composite,
    resolve_composite_anchor,
)
from PIL import Image


def _hero(path: Path) -> Path:
    Image.new("RGB", (400, 600), (230, 224, 212)).save(path, "PNG")
    return path


def _product(path: Path) -> Path:
    image = Image.new("RGBA", (100, 140), (0, 0, 0, 0))
    for x in range(18, 82):
        for y in range(45, 125):
            image.putpixel((x, y), (24, 24, 26, 255))
    image.save(path, "PNG")
    return path


def _action() -> ActionRef:
    return ActionRef(
        id="standing_right_hand_visible",
        name="Standing Right Hand Visible",
        prompt_fragment="Final catalog action.",
        camera_motion="locked",
        product_interaction="manual composite",
        loop_policy="ping_pong",
        composite_anchor=CompositeAnchor(
            anchor_id="test_anchor",
            x_ratio=0.6,
            y_ratio=0.6,
            scale_ratio=0.25,
            rotation_degrees=0.0,
            layer_order="foreground",
            notes=["test anchor"],
        ),
    )


def _preset_action() -> ActionRef:
    return ActionRef(
        id="standing_right_hand_visible",
        name="Standing Right Hand Visible",
        prompt_fragment="Final catalog action.",
        camera_motion="locked",
        product_interaction="manual composite",
        loop_policy="ping_pong",
        default_composite_anchor_id="anchor_b",
        composite_anchors=[
            CompositeAnchor(
                anchor_id="anchor_a",
                x_ratio=0.5,
                y_ratio=0.5,
                scale_ratio=0.2,
            ),
            CompositeAnchor(
                anchor_id="anchor_b",
                x_ratio=0.6,
                y_ratio=0.6,
                scale_ratio=0.25,
            ),
        ],
    )


def test_product_composite_creates_png_with_metadata(tmp_path) -> None:
    hero_path = _hero(tmp_path / "hero.png")
    product_path = _product(tmp_path / "product.png")
    output_path = tmp_path / "composite.png"
    product = ProductRef(
        id="test_bag",
        name="Test Bag",
        category="handbag",
        description="Test product",
        image_path=product_path.as_posix(),
        preservation_notes="Preserve product.",
    )

    result = render_product_locked_composite(hero_path, product, _action(), output_path)

    assert result.success is True
    assert output_path.exists()
    with Image.open(output_path) as image:
        assert image.size == (400, 600)
    assert result.anchor_id == "test_anchor"
    assert result.product_has_alpha is True
    assert result.product_alpha_bbox is not None
    assert result.freeze_core_pixels is True
    assert result.destructive_diffusion_allowed is False
    assert 0 <= result.x <= 400
    assert 0 <= result.y <= 600
    assert result.width == 100


def test_product_composite_missing_product_falls_back(tmp_path) -> None:
    hero_path = _hero(tmp_path / "hero.png")
    output_path = tmp_path / "composite.png"
    product = ProductRef(
        id="missing_bag",
        name="Missing Bag",
        category="handbag",
        description="Missing product",
        image_path=(tmp_path / "missing.png").as_posix(),
        preservation_notes="Preserve product.",
    )

    result = render_product_locked_composite(hero_path, product, _action(), output_path)

    assert output_path.exists()
    assert result.product_source_path is None
    assert any("Missing product image path" in note for note in result.notes)
    assert result.freeze_core_pixels is True


def test_compositor_uses_selected_anchor_override(tmp_path) -> None:
    hero_path = _hero(tmp_path / "hero.png")
    product_path = _product(tmp_path / "product.png")
    product = ProductRef(
        id="test_bag",
        name="Test Bag",
        category="handbag",
        description="Test product",
        image_path=product_path.as_posix(),
        preservation_notes="Preserve product.",
    )

    result = render_product_locked_composite(
        hero_path,
        product,
        _preset_action(),
        tmp_path / "composite.png",
        anchor_id="anchor_a",
    )

    assert result.anchor_id == "anchor_a"
    assert result.anchor_override_used is True
    assert result.default_anchor_used is False
    assert result.x_ratio == 0.5


def test_missing_anchor_falls_back_with_note() -> None:
    anchor, default_used, override_used, missing, notes = resolve_composite_anchor(
        _preset_action(),
        "missing_anchor",
    )

    assert anchor.anchor_id == "anchor_b"
    assert default_used is True
    assert override_used is False
    assert missing is True
    assert any("was not found" in note for note in notes)
