from backend.app.contracts import GenerationMode


def _validate_dimension(value: int, name: str) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    if value % 8 != 0:
        raise ValueError(f"{name} must be a multiple of 8")


def _profile_default_dimensions(aspect_ratio: str, profile_id: str, mode: str) -> tuple[int, int]:
    if aspect_ratio not in {"1:1", "9:16"}:
        raise ValueError(f"Unsupported aspect ratio: {aspect_ratio}")

    quality = mode == GenerationMode.quality.value

    if profile_id == "sdxl_turbo_preview":
        return (512, 512) if aspect_ratio == "1:1" else (512, 768)

    if profile_id == "sdxl_base_quality":
        if aspect_ratio == "1:1":
            return (1024, 1024) if quality else (768, 768)
        return (768, 1152) if quality else (512, 768)

    if profile_id == "flux_schnell_quality_gated":
        if aspect_ratio == "1:1":
            return (1024, 1024) if quality else (512, 512)
        return (768, 1152) if quality else (512, 768)

    if aspect_ratio == "1:1":
        return (1024, 1024) if quality else (512, 512)
    return (768, 1152) if quality else (512, 768)


def resolve_generation_dimensions(
    aspect_ratio: str,
    profile_id: str,
    mode: str,
    requested_width: int | None = None,
    requested_height: int | None = None,
) -> tuple[int, int]:
    if requested_width is not None or requested_height is not None:
        if requested_width is None or requested_height is None:
            raise ValueError("Explicit dimensions require both width and height")
        _validate_dimension(requested_width, "width")
        _validate_dimension(requested_height, "height")
        return requested_width, requested_height

    width, height = _profile_default_dimensions(aspect_ratio, profile_id, mode)
    _validate_dimension(width, "width")
    _validate_dimension(height, "height")
    return width, height
