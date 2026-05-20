from pathlib import Path

from PIL import Image
from pydantic import BaseModel, Field

from backend.app.config import project_root
from backend.app.contracts import ActionRef, CompositeAnchor, ProductRef
from backend.app.pipeline.product_assets import load_product_layer


class ProductCompositeResult(BaseModel):
    success: bool
    used_real_composite: bool = True
    output_path: Path
    product_source_path: str | None
    anchor_id: str
    x: int
    y: int
    width: int
    height: int
    scale_ratio: float
    rotation_degrees: float
    layer_order: str
    composite_method: str = "manual_anchor_alpha_overlay_v1"
    product_locked: bool = True
    freeze_core_pixels: bool = True
    destructive_diffusion_allowed: bool = False
    notes: list[str] = Field(default_factory=list)


def _default_anchor() -> CompositeAnchor:
    return CompositeAnchor(
        anchor_id="default_right_hand_side_v1",
        x_ratio=0.62,
        y_ratio=0.62,
        scale_ratio=0.22,
        rotation_degrees=0.0,
        layer_order="foreground",
        notes=["Default v1 manual anchor used because action metadata did not specify one."],
    )


def _resize_product(
    product_image: Image.Image,
    hero_size: tuple[int, int],
    scale: float,
) -> Image.Image:
    target_width = max(1, round(hero_size[0] * scale))
    ratio = target_width / product_image.width
    target_height = max(1, round(product_image.height * ratio))
    return product_image.resize((target_width, target_height), Image.Resampling.LANCZOS)


def _placement(
    hero_size: tuple[int, int],
    layer_size: tuple[int, int],
    anchor: CompositeAnchor,
) -> tuple[int, int]:
    center_x = round(hero_size[0] * anchor.x_ratio)
    center_y = round(hero_size[1] * anchor.y_ratio)
    x = center_x - layer_size[0] // 2
    y = center_y - layer_size[1] // 2
    x = min(max(0, x), max(0, hero_size[0] - layer_size[0]))
    y = min(max(0, y), max(0, hero_size[1] - layer_size[1]))
    return x, y


def _display_path(path: Path | None) -> str | None:
    if path is None:
        return None
    try:
        return path.relative_to(project_root()).as_posix()
    except ValueError:
        return path.as_posix()


def render_product_locked_composite(
    hero_still_path: Path,
    product: ProductRef,
    action: ActionRef,
    output_path: Path,
) -> ProductCompositeResult:
    """Render a deterministic v1 product-locked composite.

    The product is a controlled alpha layer. No diffusion, relighting, background
    removal, or product pixel synthesis is applied.
    """

    hero = Image.open(hero_still_path).convert("RGBA")
    product_layer = load_product_layer(product)
    anchor = action.composite_anchor or _default_anchor()

    layer = _resize_product(product_layer.image, hero.size, anchor.scale_ratio)
    if anchor.rotation_degrees:
        layer = layer.rotate(
            anchor.rotation_degrees,
            expand=True,
            resample=Image.Resampling.BICUBIC,
        )

    x, y = _placement(hero.size, layer.size, anchor)
    composite = hero.copy()
    composite.alpha_composite(layer, (x, y))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    composite.convert("RGB").save(output_path, "PNG")

    return ProductCompositeResult(
        success=True,
        output_path=output_path,
        product_source_path=_display_path(product_layer.source_path),
        anchor_id=anchor.anchor_id,
        x=x,
        y=y,
        width=layer.width,
        height=layer.height,
        scale_ratio=anchor.scale_ratio,
        rotation_degrees=anchor.rotation_degrees,
        layer_order=anchor.layer_order,
        notes=[
            *product_layer.notes,
            *anchor.notes,
            "Product layer composited by manual anchor alpha overlay.",
            "No diffusion or relighting was applied to the product layer.",
        ],
    )
