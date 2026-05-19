from backend.app.contracts import EvalResult, ProductRef


def build_product_freeze_policy(
    product: ProductRef,
) -> dict[str, str | bool | list[str] | None]:
    """Describe how product pixels should be protected in future generation stages."""

    return {
        "product_id": product.id,
        "mask_path": product.mask_path,
        "freeze_core_pixels": True,
        "allow_edge_feathering": True,
        "allow_contact_shadow": True,
        "destructive_diffusion_allowed": False,
        "notes": [
            "Protect source product silhouette, logo area, structure, straps, and hardware.",
            "Placeholder composite does not run diffusion over product pixels.",
        ],
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
