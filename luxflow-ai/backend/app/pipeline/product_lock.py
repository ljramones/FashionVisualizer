from backend.app.contracts import EvalResult, ProductRef


def build_product_freeze_policy(product: ProductRef) -> dict[str, str | bool | None]:
    """Describe how product pixels should be protected in future generation stages."""

    return {
        "product_id": product.id,
        "requires_mask": True,
        "mask_path": product.mask_path,
        "policy": "protect source product silhouette, logo area, structure, straps, and hardware",
    }


def validate_product_preservation(product: ProductRef, artifact_path: str) -> EvalResult:
    """Placeholder for future similarity checks against source handbag imagery.

    Product pixels are intended to be protected from destructive diffusion through masks,
    overlays, product-locked compositing, and later video projection.
    """

    return EvalResult(
        notes=[
            f"Product preservation validation is stubbed for {product.id}.",
            f"Future pass will compare source product assets with {artifact_path}.",
        ]
    )
