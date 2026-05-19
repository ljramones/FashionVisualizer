from backend.app.contracts import CatalogEntry


def publish_catalog_entry(entry: CatalogEntry) -> CatalogEntry:
    """Return the entry unchanged until persistent catalog writes are implemented."""

    return entry
