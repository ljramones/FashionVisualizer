import argparse
from pathlib import Path

from backend.app.config import project_root
from PIL import Image, ImageDraw


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare hero still and product composite.")
    parser.add_argument("output", help="Output directory path or request hash.")
    parser.add_argument(
        "--no-image",
        action="store_true",
        help="Only print paths; do not create hero_vs_composite.png.",
    )
    return parser.parse_args()


def resolve_output_dir(value: str) -> Path:
    candidate = Path(value)
    if candidate.exists():
        return candidate if candidate.is_absolute() else project_root() / candidate
    return project_root() / "assets/outputs" / value


def display_path(path: Path) -> str:
    try:
        return path.relative_to(project_root()).as_posix()
    except ValueError:
        return path.as_posix()


def make_comparison(hero_path: Path, composite_path: Path, output_path: Path) -> None:
    with Image.open(hero_path).convert("RGB") as hero:
        with Image.open(composite_path).convert("RGB") as composite:
            target_height = max(hero.height, composite.height)
            width = hero.width + composite.width
            label_height = 42
            sheet = Image.new("RGB", (width, target_height + label_height), (245, 242, 235))
            sheet.paste(hero, (0, label_height))
            sheet.paste(composite, (hero.width, label_height))
            draw = ImageDraw.Draw(sheet)
            draw.text((12, 14), "Hero Still", fill=(24, 24, 24))
            draw.text((hero.width + 12, 14), "Product-Locked Composite", fill=(24, 24, 24))
            sheet.save(output_path, "PNG")


def main() -> None:
    args = parse_args()
    output_dir = resolve_output_dir(args.output)
    hero_path = output_dir / "hero_still.png"
    composite_path = output_dir / "product_locked_composite.png"
    thumbnail_path = output_dir / "thumbnail.png"
    comparison_path = output_dir / "hero_vs_composite.png"

    print(f"output_directory: {display_path(output_dir)}")
    print(f"hero_still: {display_path(hero_path)}")
    print(f"product_locked_composite: {display_path(composite_path)}")
    print(f"thumbnail: {display_path(thumbnail_path)}")

    if not hero_path.exists() or not composite_path.exists():
        raise FileNotFoundError("Expected hero_still.png and product_locked_composite.png.")

    if not args.no_image:
        make_comparison(hero_path, composite_path, comparison_path)
        print(f"comparison: {display_path(comparison_path)}")


if __name__ == "__main__":
    main()
