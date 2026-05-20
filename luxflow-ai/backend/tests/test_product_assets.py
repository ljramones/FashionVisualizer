from pathlib import Path

from backend.app.contracts import ProductRef
from backend.app.pipeline.product_assets import load_product_layer
from PIL import Image


def _product(image_path: str) -> ProductRef:
    return ProductRef(
        id="test_product",
        name="Test Product",
        category="handbag",
        description="Test product.",
        image_path=image_path,
        preservation_notes="Preserve product.",
    )


def test_alpha_png_loads_rgba_with_alpha_metadata(tmp_path) -> None:
    path = tmp_path / "alpha.png"
    image = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    image.putpixel((10, 10), (20, 20, 20, 255))
    image.save(path, "PNG")

    layer = load_product_layer(_product(path.as_posix()))

    assert layer.image.mode == "RGBA"
    assert layer.has_alpha is True
    assert layer.alpha_bbox == (10, 10, 11, 11)
    assert layer.fallback_used is False


def test_rectangular_placeholder_records_no_alpha_note(tmp_path) -> None:
    path = tmp_path / "rect.png"
    Image.new("RGB", (32, 32), (20, 20, 20)).save(path, "PNG")

    layer = load_product_layer(_product(path.as_posix()))

    assert layer.image.mode == "RGBA"
    assert layer.has_alpha is False
    assert layer.alpha_bbox == (0, 0, 32, 32)
    assert any("no alpha" in note for note in layer.notes)


def test_missing_product_falls_back_cleanly(tmp_path) -> None:
    missing = tmp_path / "missing.png"

    layer = load_product_layer(_product(missing.as_posix()))

    assert layer.fallback_used is True
    assert layer.has_alpha is True
    assert layer.source_path is None


def test_tracked_alpha_assets_exist_and_have_alpha() -> None:
    for path in [
        Path("assets/products/handbags/black_structured_bag/product_alpha.png"),
        Path("assets/products/handbags/tan_travel_tote/product_alpha.png"),
        Path("assets/products/handbags/evening_clutch/product_alpha.png"),
    ]:
        layer = load_product_layer(_product(path.as_posix()))
        assert layer.has_alpha is True
        assert layer.alpha_bbox is not None
