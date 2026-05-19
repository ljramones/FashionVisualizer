from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from backend.app.config import resolve_project_path
from backend.app.contracts import SceneRecipe

CANVAS_SIZE = 1024
THUMBNAIL_SIZE = 512


def _palette(request_hash: str) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    seed = int(request_hash[:6], 16)
    primary = (40 + seed % 90, 48 + (seed >> 3) % 70, 58 + (seed >> 6) % 70)
    accent = (160 + (seed >> 2) % 70, 130 + (seed >> 5) % 80, 90 + (seed >> 8) % 80)
    return primary, accent


def _font(size: int) -> ImageFont.ImageFont | ImageFont.FreeTypeFont:
    del size
    return ImageFont.load_default()


def _wrap_text(text: str, max_chars: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    line = ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if len(candidate) > max_chars and line:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines


def _draw_lines(
    draw: ImageDraw.ImageDraw,
    lines: list[str],
    origin: tuple[int, int],
    fill: tuple[int, int, int],
    spacing: int = 24,
) -> None:
    x, y = origin
    for line in lines:
        draw.text((x, y), line, fill=fill, font=_font(18))
        y += spacing


def _paste_product_placeholder(
    image: Image.Image,
    recipe: SceneRecipe,
    box: tuple[int, int],
) -> None:
    if recipe.product.image_path is None:
        return
    product_path = resolve_project_path(Path(recipe.product.image_path))
    if not product_path.exists():
        return
    product = Image.open(product_path).convert("RGBA")
    product.thumbnail(box)
    x = image.width - product.width - 96
    y = image.height - product.height - 118
    image.alpha_composite(product, (x, y))


def _base_scene(recipe: SceneRecipe, title: str) -> Image.Image:
    primary, accent = _palette(recipe.request_hash)
    image = Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), primary + (255,))
    draw = ImageDraw.Draw(image)

    draw.rectangle((48, 48, 976, 976), outline=(242, 235, 220), width=4)
    draw.rectangle((80, 80, 944, 260), fill=(255, 255, 255, 235))
    draw.text((112, 112), title, fill=(24, 28, 34), font=_font(28))
    draw.text(
        (112, 156),
        f"{recipe.product.name} | {recipe.mode.value} | {recipe.request_hash[:8]}",
        fill=(72, 76, 82),
        font=_font(18),
    )

    draw.rounded_rectangle((112, 324, 592, 790), radius=24, fill=(245, 241, 232, 255))
    draw.rectangle((132, 604, 572, 760), fill=accent + (255,))
    draw.ellipse((282, 400, 422, 540), fill=(205, 197, 184, 255))
    draw.line((352, 540, 352, 690), fill=(80, 74, 70), width=10)
    draw.line((352, 620, 458, 704), fill=(80, 74, 70), width=8)
    draw.line((352, 620, 246, 704), fill=(80, 74, 70), width=8)

    lines = [
        f"Model: {recipe.model.display_name}",
        f"Location: {recipe.location.name}",
        f"Action: {recipe.action.name}",
        f"Lighting: {recipe.location.lighting}",
        f"Camera: {recipe.action.camera_motion}",
    ]
    _draw_lines(draw, lines, (112, 820), (245, 241, 232), spacing=28)
    return image


def render_hero_still_placeholder(recipe: SceneRecipe, output_path: Path) -> Path:
    """Render a deterministic hero still placeholder; no ML model is invoked."""

    image = _base_scene(recipe, "HERO STILL PLACEHOLDER")
    draw = ImageDraw.Draw(image)
    _draw_lines(
        draw,
        _wrap_text(recipe.location.prompt_fragment, 44),
        (640, 324),
        (248, 244, 235),
        spacing=26,
    )
    _paste_product_placeholder(image, recipe, (280, 280))
    image.convert("RGB").save(output_path, "PNG")
    return output_path


def render_product_locked_composite_placeholder(recipe: SceneRecipe, output_path: Path) -> Path:
    """Render a deterministic composite placeholder showing product-lock intent."""

    image = _base_scene(recipe, "PRODUCT-LOCKED COMPOSITE")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((630, 350, 900, 690), radius=28, fill=(24, 24, 26, 255))
    draw.rounded_rectangle((680, 475, 850, 635), radius=18, outline=(255, 236, 170), width=8)
    draw.arc((716, 420, 814, 530), 180, 360, fill=(255, 236, 170), width=8)
    draw.text((650, 720), "PRODUCT LOCKED LAYER", fill=(255, 236, 170), font=_font(18))
    _draw_lines(
        draw,
        _wrap_text(recipe.product.preservation_notes, 36),
        (640, 780),
        (248, 244, 235),
        spacing=24,
    )
    _paste_product_placeholder(image, recipe, (230, 230))
    image.convert("RGB").save(output_path, "PNG")
    return output_path


def render_thumbnail(composite_path: Path, output_path: Path) -> Path:
    """Render a smaller thumbnail from the product-locked composite."""

    image = Image.open(composite_path).convert("RGB")
    image.thumbnail((THUMBNAIL_SIZE, THUMBNAIL_SIZE))
    thumb = Image.new("RGB", (THUMBNAIL_SIZE, THUMBNAIL_SIZE), (28, 30, 34))
    x = (THUMBNAIL_SIZE - image.width) // 2
    y = (THUMBNAIL_SIZE - image.height) // 2
    thumb.paste(image, (x, y))
    thumb.save(output_path, "PNG")
    return output_path
