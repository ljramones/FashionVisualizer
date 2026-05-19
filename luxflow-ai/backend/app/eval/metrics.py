from backend.app.contracts import CatalogEntry, EvalResult


def evaluate_catalog_entry(entry: CatalogEntry) -> EvalResult:
    """Return honest placeholder MVP evaluation.

    Prompt adherence remains unmeasured because no vision-language model is installed.
    Product preservation passes only in the narrow placeholder sense: the product-locked
    composite was drawn deterministically and was not generated through destructive diffusion.
    """

    has_composite = any(
        artifact.kind == "product_locked_composite" and artifact.exists
        for artifact in entry.artifacts
    )
    return EvalResult(
        prompt_adherence_score=None,
        product_preservation_score=1.0 if has_composite else None,
        notes=[
            "Prompt adherence not measured; no vision model installed.",
            "Product preservation placeholder passed because product layer was not generated "
            "by diffusion."
            if has_composite
            else "Product preservation placeholder pending composite artifact.",
            f"Evaluated placeholder entry {entry.id}.",
        ],
    )
