import pytest
from backend.app.generation.dimensions import resolve_generation_dimensions


def test_preview_square_dimensions_are_multiple_of_8() -> None:
    width, height = resolve_generation_dimensions("1:1", "sdxl_turbo_preview", "preview")

    assert (width, height) == (512, 512)
    assert width % 8 == 0
    assert height % 8 == 0


def test_preview_portrait_dimensions_are_not_square() -> None:
    width, height = resolve_generation_dimensions("9:16", "sdxl_turbo_preview", "preview")

    assert height > width
    assert (width, height) == (512, 768)


def test_quality_portrait_dimensions_for_sdxl_base() -> None:
    width, height = resolve_generation_dimensions("9:16", "sdxl_base_quality", "quality")

    assert (width, height) == (768, 1152)
    assert width % 8 == 0
    assert height % 8 == 0


def test_explicit_dimension_overrides_are_respected() -> None:
    assert resolve_generation_dimensions(
        "9:16",
        "sdxl_turbo_preview",
        "preview",
        requested_width=640,
        requested_height=896,
    ) == (640, 896)


def test_invalid_aspect_ratio_fails_cleanly() -> None:
    with pytest.raises(ValueError, match="Unsupported aspect ratio"):
        resolve_generation_dimensions("16:9", "sdxl_turbo_preview", "preview")


def test_invalid_dimension_override_fails_cleanly() -> None:
    with pytest.raises(ValueError, match="multiple of 8"):
        resolve_generation_dimensions(
            "9:16",
            "sdxl_turbo_preview",
            "preview",
            requested_width=513,
            requested_height=768,
        )
