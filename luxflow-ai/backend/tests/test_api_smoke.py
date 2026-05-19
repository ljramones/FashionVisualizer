from backend.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_core_get_endpoints_return_json() -> None:
    for path in [
        "/health",
        "/system/capabilities",
        "/catalog",
        "/assets/products",
        "/assets/models",
        "/assets/locations",
        "/assets/actions",
    ]:
        response = client.get(path)

        assert response.status_code == 200
        assert response.headers["content-type"].startswith("application/json")


def test_compile_and_generate_endpoints_return_json() -> None:
    request = {
        "product_id": "black_structured_bag",
        "model_id": "adult_female_editorial_01",
        "location_id": "hotel_lobby",
        "action_id": "walking_with_bag",
        "seed": 42,
        "aspect_ratio": "9:16",
        "mode": "preview",
    }

    compile_response = client.post("/recipes/compile", json=request)
    generate_response = client.post("/generate", json=request)

    assert compile_response.status_code == 200
    assert compile_response.json()["request_hash"]
    assert generate_response.status_code == 200
    assert generate_response.json()["route"]["name"] == "handbag_diffusers_reference"
    assert generate_response.json()["status"] == "stub"
