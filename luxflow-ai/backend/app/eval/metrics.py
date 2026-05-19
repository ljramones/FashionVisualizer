from backend.app.contracts import CatalogEntry, EvalResult


def evaluate_catalog_entry(entry: CatalogEntry) -> EvalResult:
    """Return placeholder MVP evaluation.

    MVP metrics are prompt adherence and product preservation/similarity. Scores remain None
    until real generated artifacts exist and can be compared against the compiled recipe and
    source product assets.
    """

    return EvalResult(
        prompt_adherence_score=None,
        product_preservation_score=None,
        notes=[
            "Prompt adherence score pending real generation output.",
            "Product preservation score pending image similarity implementation.",
            f"Evaluated placeholder entry {entry.id}.",
        ],
    )
