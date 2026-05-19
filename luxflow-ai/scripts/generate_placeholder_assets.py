from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _write_png(path: Path, label: str, color: tuple[int, int, int]) -> None:
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        readme = path.with_suffix(".md")
        readme.write_text(
            f"# Placeholder\n\nInstall Pillow to generate `{path.name}` for {label}.\n"
        )
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (640, 800), color)
    draw = ImageDraw.Draw(image)
    draw.rectangle((140, 260, 500, 560), outline=(255, 255, 255), width=6)
    draw.text((170, 380), label, fill=(255, 255, 255))
    image.save(path)


def main() -> None:
    placeholders = [
        (
            ROOT / "assets/products/handbags/black_structured_bag/placeholder.png",
            "Black Structured Bag",
            (24, 24, 28),
        ),
        (
            ROOT / "assets/products/handbags/tan_travel_tote/placeholder.png",
            "Tan Travel Tote",
            (166, 119, 73),
        ),
        (
            ROOT / "assets/products/handbags/evening_clutch/placeholder.png",
            "Evening Clutch",
            (70, 62, 86),
        ),
        (
            ROOT / "assets/models/adult_female_editorial_01/placeholder.png",
            "Synthetic Female Profile",
            (92, 105, 128),
        ),
        (
            ROOT / "assets/models/adult_male_editorial_01/placeholder.png",
            "Synthetic Male Profile",
            (72, 88, 104),
        ),
        (ROOT / "assets/locations/hotel_lobby/placeholder.png", "Hotel Lobby", (120, 96, 72)),
        (
            ROOT / "assets/locations/modern_gallery/placeholder.png",
            "Modern Gallery",
            (215, 215, 208),
        ),
    ]
    for path, label, color in placeholders:
        _write_png(path, label, color)
    print("Generated placeholder asset files where Pillow is available.")


if __name__ == "__main__":
    main()
