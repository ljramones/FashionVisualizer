import json
from pathlib import Path
from typing import cast
from typing import TypeVar

from pydantic import BaseModel

from backend.app.config import resolve_project_path, settings
from backend.app.contracts import ActionRef, LocationRef, ModelProfile, ProductRef

T = TypeVar("T", bound=BaseModel)


def _load_metadata_file(path: Path, model: type[T]) -> T:
    with path.open("r", encoding="utf-8") as handle:
        return model.model_validate(json.load(handle))


def _load_metadata_dir(relative_path: str, model: type[T]) -> list[T]:
    base = resolve_project_path(settings.assets_dir) / relative_path
    if not base.exists():
        return []
    items: list[T] = []
    for metadata_path in sorted(base.glob("*/metadata.json")):
        items.append(_load_metadata_file(metadata_path, model))
    return items


def load_products() -> list[ProductRef]:
    return _load_metadata_dir("products/handbags", ProductRef)


def load_models() -> list[ModelProfile]:
    return _load_metadata_dir("models", ModelProfile)


def load_locations() -> list[LocationRef]:
    return _load_metadata_dir("locations", LocationRef)


def load_actions() -> list[ActionRef]:
    return _load_metadata_dir("actions", ActionRef)


def _find_by_id(items: list[T], item_id: str, label: str) -> T:
    for item in items:
        if getattr(item, "id") == item_id:
            return item
    raise KeyError(f"Unknown {label}: {item_id}")


def get_product(product_id: str) -> ProductRef:
    return _find_by_id(load_products(), product_id, "product")


def get_model(model_id: str) -> ModelProfile:
    return _find_by_id(load_models(), model_id, "model")


def get_location(location_id: str) -> LocationRef:
    return _find_by_id(load_locations(), location_id, "location")


def get_action(action_id: str) -> ActionRef:
    return _find_by_id(load_actions(), action_id, "action")


def load_catalog() -> dict[str, object]:
    catalog_path = resolve_project_path(settings.catalog_path)
    if not catalog_path.exists():
        return {"entries": []}
    with catalog_path.open("r", encoding="utf-8") as handle:
        return cast(dict[str, object], json.load(handle))
