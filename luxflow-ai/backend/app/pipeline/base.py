from typing import Protocol

from backend.app.contracts import CatalogEntry, SceneRecipe


class Pipeline(Protocol):
    def run(self, recipe: SceneRecipe) -> CatalogEntry:
        """Run a pipeline and return a catalog entry."""
        ...
