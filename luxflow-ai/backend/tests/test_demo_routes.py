from pathlib import Path

from backend.app.config import settings
from backend.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_get_golden_recipe_returns_expected_ids() -> None:
    response = client.get("/demo/golden-recipe")

    assert response.status_code == 200
    recipe = response.json()
    assert recipe["product_id"] == "black_structured_bag"
    assert recipe["model_id"] == "adult_female_editorial_01"
    assert recipe["location_id"] == "hotel_lobby"
    assert recipe["action_id"] == "walking_with_bag"
    assert recipe["seed"] == 42
    assert recipe["aspect_ratio"] == "9:16"
    assert recipe["mode"] == "preview"


def test_run_golden_demo_creates_artifacts(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(settings, "output_root", tmp_path)

    response = client.post("/demo/run-golden")

    assert response.status_code == 200
    entry = response.json()
    output_dir = tmp_path / entry["recipe_hash"]
    assert output_dir.exists()

    artifacts = {artifact["kind"]: artifact for artifact in entry["artifacts"]}
    assert Path(artifacts["thumbnail"]["path"]).exists()
    assert Path(artifacts["pipeline_trace"]["path"]).exists()
    assert artifacts["thumbnail"]["static_url"] is None
    assert entry["route"]["name"] == "handbag_diffusers_reference_stub"
