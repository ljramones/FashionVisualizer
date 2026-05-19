import json

import pytest
from backend.app.contracts import ProductCategory
from backend.app.registry import asset_registry
from backend.app.registry.asset_registry import MetadataLoadError


def test_registry_loads_products_from_project_assets() -> None:
    products = asset_registry.load_products()

    assert products
    assert products[0].category == ProductCategory.handbag


def test_missing_metadata_directory_returns_empty_list(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(asset_registry.settings, "assets_dir", tmp_path)

    assert asset_registry.load_products() == []


def test_invalid_json_reports_metadata_path(tmp_path, monkeypatch) -> None:
    metadata_dir = tmp_path / "products/handbags/bad_bag"
    metadata_dir.mkdir(parents=True)
    metadata_path = metadata_dir / "metadata.json"
    metadata_path.write_text("{not json", encoding="utf-8")
    monkeypatch.setattr(asset_registry.settings, "assets_dir", tmp_path)

    with pytest.raises(MetadataLoadError, match="Invalid JSON in metadata file"):
        asset_registry.load_products()


def test_valid_json_with_invalid_schema_reports_contract(tmp_path, monkeypatch) -> None:
    metadata_dir = tmp_path / "products/handbags/bad_bag"
    metadata_dir.mkdir(parents=True)
    (metadata_dir / "metadata.json").write_text(json.dumps({"id": "bad_bag"}), encoding="utf-8")
    monkeypatch.setattr(asset_registry.settings, "assets_dir", tmp_path)

    with pytest.raises(MetadataLoadError, match="Invalid ProductRef metadata"):
        asset_registry.load_products()
