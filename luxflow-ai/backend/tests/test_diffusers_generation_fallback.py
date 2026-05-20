import json

from backend.app.config import settings
from backend.app.contracts import GenerationRequest
from backend.app.main import app
from backend.app.pipeline.handbag_pipeline import run_handbag_pipeline
from backend.app.recipes.scene_recipe_compiler import compile_scene_recipe
from fastapi.testclient import TestClient

client = TestClient(app)


def _recipe():
    return compile_scene_recipe(
        GenerationRequest(
            product_id="black_structured_bag",
            model_id="adult_female_editorial_01",
            location_id="hotel_lobby",
            action_id="walking_with_bag",
        )
    )


def test_generation_disabled_uses_placeholder(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(settings, "enable_real_image_generation", False)

    entry = run_handbag_pipeline(_recipe(), output_root=tmp_path)
    trace_path = tmp_path / entry.recipe_hash / "pipeline_trace.json"
    trace = json.loads(trace_path.read_text(encoding="utf-8"))

    assert trace["hero_still_generation"]["real_generation_enabled"] is False
    assert trace["hero_still_generation"]["generation_attempted"] is False
    assert trace["hero_still_generation"]["used_real_generation"] is False
    assert trace["hero_still_generation"]["fallback_used"] is True
    assert trace["hero_still_generation"]["duration_seconds"] is not None
    assert "dependency_status" in trace["hero_still_generation"]
    assert trace["stages"][1]["label"] == "Hero still placeholder rendered"


def test_missing_diffusers_falls_back_cleanly(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(settings, "enable_real_image_generation", True)
    monkeypatch.setattr(
        "backend.app.pipeline.handbag_pipeline.generate_hero_still_with_diffusers",
        lambda recipe, output_path: type(
            "Result",
            (),
            {
                "success": False,
                "output_path": None,
                "model_id": settings.image_model_id,
                "device": "cpu",
                "profile_id": "sdxl_turbo_preview",
                "positive_prompt_preview": "positive preview",
                "negative_prompt_preview": "negative preview",
                "width": 512,
                "height": 768,
                "steps": 2,
                "guidance_scale": 0.0,
                "supports_negative_prompt": False,
                "prompt_profile_used": "sdxl_turbo_preview",
                "prompt_strategy": "product_empty_scene_for_later_composite",
                "aspect_ratio_requested": "9:16",
                "aspect_ratio_resolved": "9:16",
                "dependency_status": {
                    "torch_available": False,
                    "diffusers_available": False,
                    "torch_version": None,
                    "diffusers_version": None,
                    "mps_available": False,
                    "cuda_available": False,
                },
                "notes": ["diffusers missing in test"],
                "error": "No module named diffusers",
            },
        )(),
    )

    entry = run_handbag_pipeline(_recipe(), output_root=tmp_path)
    trace_path = tmp_path / entry.recipe_hash / "pipeline_trace.json"
    trace = json.loads(trace_path.read_text(encoding="utf-8"))

    assert (tmp_path / entry.recipe_hash / "hero_still.png").exists()
    assert trace["hero_still_generation"]["real_generation_enabled"] is True
    assert trace["hero_still_generation"]["generation_attempted"] is True
    assert trace["hero_still_generation"]["used_real_generation"] is False
    assert trace["hero_still_generation"]["fallback_used"] is True
    assert trace["hero_still_generation"]["error_summary"] == "No module named diffusers"
    assert trace["hero_still_generation"]["profile_id"] == "sdxl_turbo_preview"
    assert trace["hero_still_generation"]["width"] == 512
    assert trace["hero_still_generation"]["height"] == 768
    assert trace["hero_still_generation"]["prompt_strategy"] == (
        "product_empty_scene_for_later_composite"
    )
    assert "diffusers missing in test" in trace["hero_still_generation"]["notes"]


def test_system_capabilities_generation_fields_do_not_crash() -> None:
    response = client.get("/system/capabilities")

    assert response.status_code == 200
    payload = response.json()
    assert "real_image_generation_enabled" in payload
    assert "generation_dependencies_available" in payload
    assert "mps_available" in payload
    assert "cuda_available" in payload
