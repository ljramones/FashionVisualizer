from pathlib import Path

from backend.app.config import settings
from backend.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def _request() -> dict[str, object]:
    return {
        "product_id": "black_structured_bag",
        "model_id": "adult_female_editorial_01",
        "location_id": "hotel_lobby",
        "action_id": "walking_with_bag",
        "seed": 42,
        "aspect_ratio": "9:16",
        "mode": "preview",
    }


def test_generate_creates_deterministic_artifacts(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(settings, "output_root", tmp_path)

    first_response = client.post("/generate", json=_request())
    second_response = client.post("/generate", json=_request())

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    first = first_response.json()
    second = second_response.json()
    assert first["recipe_hash"] == second["recipe_hash"]
    output_dir = tmp_path / first["recipe_hash"]
    assert output_dir.exists()

    expected_files = {
        "hero_still.png",
        "product_locked_composite.png",
        "thumbnail.png",
        "final_video_placeholder.json",
        "catalog_entry.json",
        "pipeline_trace.json",
    }
    assert expected_files == {path.name for path in output_dir.iterdir()}

    artifacts = {artifact["kind"]: artifact for artifact in first["artifacts"]}
    assert Path(artifacts["hero_still"]["path"]).exists()
    assert Path(artifacts["thumbnail"]["path"]).exists()
    assert Path(artifacts["catalog_entry"]["path"]).exists()
    assert Path(artifacts["pipeline_trace"]["path"]).exists()
    assert first["eval"]["product_preservation_score"] == 1.0
