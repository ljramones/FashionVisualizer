import json

from backend.app.pipeline.artifact_store import ArtifactStore


def test_output_directory_is_deterministic(tmp_path) -> None:
    first = ArtifactStore("abc123", output_root=tmp_path)
    second = ArtifactStore("abc123", output_root=tmp_path)

    assert first.output_dir == second.output_dir
    assert first.output_dir == tmp_path / "abc123"


def test_artifact_paths_are_created_under_hash_directory(tmp_path) -> None:
    store = ArtifactStore("abc123", output_root=tmp_path)
    artifact_path = store.path_for("hero_still.png")

    assert artifact_path == tmp_path / "abc123" / "hero_still.png"
    assert artifact_path.parent.exists()


def test_json_writing_and_rerun_reuses_directory(tmp_path) -> None:
    store = ArtifactStore("abc123", output_root=tmp_path)
    first_path = store.write_json("catalog_entry.json", {"status": "first"})
    second_path = ArtifactStore("abc123", output_root=tmp_path).write_json(
        "catalog_entry.json",
        {"status": "second"},
    )

    assert first_path == second_path
    assert json.loads(second_path.read_text(encoding="utf-8")) == {"status": "second"}
