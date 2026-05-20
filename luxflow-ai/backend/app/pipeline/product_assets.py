from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from backend.app.config import resolve_project_path
from backend.app.contracts import ProductRef


@dataclass(frozen=True)
class ProductLayer:
    image: Image.Image
    mask: Image.Image | None
    width: int
    height: int
    source_path: Path | None
    notes: list[str]


def _font() -> ImageFont.ImageFont | ImageFont.FreeTypeFont:
    return ImageFont.load_default()


def _fallback_product_layer(product: ProductRef) -> ProductLayer:
    image = Image.new("RGBA", (520, 420), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((70, 120, 450, 350), radius=28, fill=(24, 24, 26, 255))
    draw.rounded_rectangle((130, 185, 390, 310), radius=14, outline=(235, 220, 180), width=8)
    draw.arc((185, 70, 335, 210), 180, 360, fill=(235, 220, 180), width=10)
    draw.text((150, 230), product.name, fill=(245, 241, 232), font=_font())
    return ProductLayer(
        image=image,
        mask=image.getchannel("A"),
        width=image.width,
        height=image.height,
        source_path=None,
        notes=[
            "Product image was missing; rendered deterministic placeholder product layer.",
            "Placeholder layer is still treated as frozen product pixels.",
        ],
    )


def load_product_layer(product: ProductRef) -> ProductLayer:
    """Load a product image as a frozen compositing layer.

    This helper intentionally does not perform ML background removal. If a product
    image has alpha, that alpha is preserved. Otherwise the whole image is used as
    an opaque rectangular layer for v1.
    """

    if product.image_path is None:
        return _fallback_product_layer(product)

    source_path = resolve_project_path(Path(product.image_path))
    if not source_path.exists():
        layer = _fallback_product_layer(product)
        layer.notes.append(f"Missing product image path: {product.image_path}")
        return layer

    image = Image.open(source_path).convert("RGBA")
    alpha = image.getchannel("A")
    notes = [f"Loaded product layer from {product.image_path}."]
    if alpha.getextrema() == (255, 255):
        notes.append(
            "Source image has no alpha; using the full rectangular image as the layer."
        )
    else:
        notes.append("Source image alpha preserved.")

    return ProductLayer(
        image=image,
        mask=alpha,
        width=image.width,
        height=image.height,
        source_path=source_path,
        notes=notes,
    )
