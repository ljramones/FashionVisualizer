from backend.app.generation.model_candidates import get_model_candidate, get_model_candidates


def test_model_candidates_are_ordered_and_include_expected_models() -> None:
    candidates = get_model_candidates()

    assert [candidate.smoke_test_priority for candidate in candidates] == sorted(
        candidate.smoke_test_priority for candidate in candidates
    )
    assert get_model_candidate("black-forest-labs/FLUX.1-schnell") is not None
    assert get_model_candidate("stabilityai/stable-diffusion-xl-base-1.0") is not None
    assert get_model_candidate("stabilityai/sdxl-turbo") is not None


def test_model_candidate_metadata_documents_access_and_license() -> None:
    flux = get_model_candidate("black-forest-labs/FLUX.1-schnell")
    turbo = get_model_candidate("stabilityai/sdxl-turbo")

    assert flux is not None
    assert turbo is not None
    assert "access" in flux.access_note.lower()
    assert "license" in turbo.license_note.lower() or "terms" in turbo.license_note.lower()
