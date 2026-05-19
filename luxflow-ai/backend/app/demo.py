import json

from backend.app.config import project_root
from backend.app.contracts import GenerationRequest

GOLDEN_RECIPE_PATH = project_root() / "assets/demo/golden_recipe.json"


def load_golden_generation_request() -> GenerationRequest:
    payload = json.loads(GOLDEN_RECIPE_PATH.read_text(encoding="utf-8"))
    return GenerationRequest.model_validate(payload)
