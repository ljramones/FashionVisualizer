import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from backend.app.config import project_root, resolve_project_path, settings


class ArtifactStore:
    """Deterministic file store for a single recipe hash."""

    def __init__(self, request_hash: str, output_root: Path | None = None) -> None:
        self.request_hash = request_hash
        root = output_root if output_root is not None else settings.output_root
        self.output_root = resolve_project_path(root)
        self.output_dir = self.output_root / request_hash

    def ensure_output_dir(self) -> Path:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        return self.output_dir

    def path_for(self, filename: str) -> Path:
        self.ensure_output_dir()
        return self.output_dir / filename

    def relative_path(self, path: Path) -> str:
        root = project_root()
        try:
            return path.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            return path.resolve().as_posix()

    def static_url(self, path: Path) -> str | None:
        relative = self.relative_path(path)
        assets_prefix = "assets/"
        if not relative.startswith(assets_prefix):
            return None
        return f"/static/assets/{relative.removeprefix(assets_prefix)}"

    def write_json(self, filename: str, payload: BaseModel | dict[str, Any]) -> Path:
        path = self.path_for(filename)
        if isinstance(payload, BaseModel):
            content = payload.model_dump(mode="json")
        else:
            content = payload
        path.write_text(json.dumps(content, indent=2) + "\n", encoding="utf-8")
        return path

    def write_text(self, filename: str, content: str) -> Path:
        path = self.path_for(filename)
        path.write_text(content, encoding="utf-8")
        return path
