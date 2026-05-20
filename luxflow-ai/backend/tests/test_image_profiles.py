from backend.app.generation.image_profiles import (
    get_image_profile,
    get_image_profiles,
    resolve_image_profile,
)


def test_image_profiles_include_expected_profiles() -> None:
    profile_ids = {profile.profile_id for profile in get_image_profiles()}

    assert "sdxl_turbo_preview" in profile_ids
    assert "sdxl_base_quality" in profile_ids
    assert "flux_schnell_quality_gated" in profile_ids


def test_profile_lookup_by_id_and_model() -> None:
    turbo = get_image_profile("sdxl_turbo_preview")

    assert turbo is not None
    assert turbo.model_id == "stabilityai/sdxl-turbo"
    assert resolve_image_profile(None, "stabilityai/sdxl-turbo").profile_id == (
        "sdxl_turbo_preview"
    )


def test_unknown_profile_fails_cleanly() -> None:
    try:
        resolve_image_profile("missing_profile", "stabilityai/sdxl-turbo")
    except ValueError as exc:
        assert "Unknown image generation profile" in str(exc)
    else:
        raise AssertionError("Expected unknown profile to raise ValueError")
