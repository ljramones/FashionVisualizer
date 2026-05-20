from dataclasses import dataclass
from pathlib import Path

from backend.app.config import project_root
from PIL import Image, ImageDraw


@dataclass(frozen=True)
class ProductAlphaSpec:
    product_id: str
    body_color: tuple[int, int, int, int]
    edge_color: tuple[int, int, int, int]
    hardware_color: tuple[int, int, int, int]
    shape: str


SPECS = [
    ProductAlphaSpec(
        product_id="black_structured_bag",
        body_color=(24, 24, 26, 255),
        edge_color=(220, 220, 225, 255),
        hardware_color=(218, 184, 104, 255),
        shape="structured",
    ),
    ProductAlphaSpec(
        product_id="tan_travel_tote",
        body_color=(176, 122, 72, 255),
        edge_color=(95, 62, 38, 255),
        hardware_color=(210, 172, 95, 255),
        shape="tote",
    ),
    ProductAlphaSpec(
        product_id="evening_clutch",
        body_color=(48, 38, 58, 255),
        edge_color=(230, 220, 235, 255),
        hardware_color=(230, 188, 118, 255),
        shape="clutch",
    ),
]


def _draw_structured(draw: ImageDraw.ImageDraw, spec: ProductAlphaSpec) -> None:
    draw.rounded_rectangle((105, 180, 395, 370), radius=26, fill=spec.body_color)
    draw.rounded_rectangle((125, 205, 375, 345), radius=14, outline=spec.edge_color, width=7)
    draw.arc((180, 105, 320, 235), 180, 360, fill=spec.edge_color, width=10)
    draw.rectangle((236, 260, 264, 281), fill=spec.hardware_color)
    draw.line((135, 180, 125, 150), fill=spec.edge_color, width=7)
    draw.line((365, 180, 375, 150), fill=spec.edge_color, width=7)


def _draw_tote(draw: ImageDraw.ImageDraw, spec: ProductAlphaSpec) -> None:
    draw.rounded_rectangle((88, 175, 412, 390), radius=36, fill=spec.body_color)
    draw.line((145, 180, 135, 95), fill=spec.edge_color, width=12)
    draw.line((355, 180, 365, 95), fill=spec.edge_color, width=12)
    draw.arc((135, 55, 365, 210), 180, 360, fill=spec.edge_color, width=12)
    draw.line((132, 205, 405, 205), fill=(210, 150, 92, 255), width=5)
    draw.rectangle((238, 270, 262, 290), fill=spec.hardware_color)


def _draw_clutch(draw: ImageDraw.ImageDraw, spec: ProductAlphaSpec) -> None:
    draw.rounded_rectangle((90, 210, 410, 330), radius=22, fill=spec.body_color)
    draw.rounded_rectangle((110, 228, 390, 312), radius=14, outline=spec.edge_color, width=6)
    draw.rectangle((225, 205, 275, 225), fill=spec.hardware_color)
    draw.line((100, 265, 400, 265), fill=(90, 75, 105, 255), width=4)


def render_product_alpha(spec: ProductAlphaSpec, output_path: Path) -> None:
    image = Image.new("RGBA", (500, 500), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    if spec.shape == "structured":
        _draw_structured(draw, spec)
    elif spec.shape == "tote":
        _draw_tote(draw, spec)
    else:
        _draw_clutch(draw, spec)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, "PNG")


def main() -> None:
    for spec in SPECS:
        output_path = (
            project_root()
            / "assets/products/handbags"
            / spec.product_id
            / "product_alpha.png"
        )
        render_product_alpha(spec, output_path)
        print(output_path.relative_to(project_root()).as_posix())


if __name__ == "__main__":
    main()
