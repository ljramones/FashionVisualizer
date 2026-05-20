import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

from backend.app.config import project_root
from backend.app.contracts import GenerationRequest
from backend.app.pipeline.handbag_pipeline import run_handbag_pipeline
from backend.app.pipeline.product_composite import render_product_locked_composite
from backend.app.recipes.scene_recipe_compiler import compile_scene_recipe
from PIL import Image, ImageDraw
from pydantic import BaseModel

DEFAULT_ANCHORS = [
    "right_hand_side_v1",
    "right_hand_side_v2",
    "right_hip_mid_v1",
    "right_hip_lower_v1",
]
DEFAULT_RECIPE = "assets/demo/golden_empty_hand_recipe.json"


class AnchorTuningResult(BaseModel):
    anchor_id: str
    output_path: str
    product_has_alpha: bool
    product_alpha_bbox: tuple[int, int, int, int] | None
    x_ratio: float
    y_ratio: float
    scale_ratio: float
    pixel_x: int
    pixel_y: int
    rendered_width: int
    rendered_height: int
    notes: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Tune manual product composite anchors.")
    parser.add_argument("--output-dir", help="Existing output directory containing hero_still.png.")
    parser.add_argument("--recipe-file", default=DEFAULT_RECIPE)
    parser.add_argument("--anchors", nargs="+", default=DEFAULT_ANCHORS)
    parser.add_argument("--run-id")
    return parser.parse_args()


def _load_recipe(recipe_file: str) -> GenerationRequest:
    payload = json.loads((project_root() / recipe_file).read_text(encoding="utf-8"))
    return GenerationRequest.model_validate(payload)


def _resolve_source_output_dir(args: argparse.Namespace, recipe_hash: str) -> Path:
    if args.output_dir:
        candidate = Path(args.output_dir)
        return candidate if candidate.is_absolute() else project_root() / candidate
    return project_root() / "assets/outputs" / recipe_hash


def _display(path: Path) -> str:
    try:
        return path.relative_to(project_root()).as_posix()
    except ValueError:
        return path.as_posix()


def _run_source_if_needed(args: argparse.Namespace, recipe_hash: str) -> Path:
    source_dir = _resolve_source_output_dir(args, recipe_hash)
    if (source_dir / "hero_still.png").exists():
        return source_dir
    recipe = compile_scene_recipe(_load_recipe(args.recipe_file))
    run_handbag_pipeline(recipe)
    return source_dir


def _make_contact_sheet(results: list[AnchorTuningResult], output_path: Path) -> None:
    thumb_width = 240
    thumb_height = 360
    label_height = 56
    columns = 2
    rows = (len(results) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * thumb_width, rows * (thumb_height + label_height)), "white")
    draw = ImageDraw.Draw(sheet)

    for index, result in enumerate(results):
        with Image.open(project_root() / result.output_path) as image:
            image.thumbnail((thumb_width, thumb_height))
            x = (index % columns) * thumb_width
            y = (index // columns) * (thumb_height + label_height)
            sheet.paste(image.convert("RGB"), (x, y))
            draw.text(
                (x + 6, y + thumb_height + 6),
                f"{result.anchor_id}\n"
                f"x {result.x_ratio} y {result.y_ratio} scale {result.scale_ratio}",
                fill=(20, 20, 20),
            )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path, "PNG")


def _write_reports(
    run_id: str,
    args: argparse.Namespace,
    source_dir: Path,
    contact_sheet: Path,
    results: list[AnchorTuningResult],
) -> None:
    report = {
        "run_id": run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "recipe_file": args.recipe_file,
        "source_output_dir": _display(source_dir),
        "hero_still": _display(source_dir / "hero_still.png"),
        "contact_sheet": _display(contact_sheet),
        "anchors": args.anchors,
        "results": [result.model_dump(mode="json") for result in results],
    }
    report_path = contact_sheet.parent / "anchor_tuning_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    docs_path = project_root() / "docs/composite_anchor_tuning_results.md"
    lines = [
        "# Composite Anchor Tuning Results",
        "",
        f"Run ID: `{run_id}`",
        f"Run timestamp: `{report['created_at']}`",
        f"Recipe: `{args.recipe_file}`",
        f"Hero still source: `{report['hero_still']}`",
        f"Contact sheet: `{report['contact_sheet']}`",
        "",
        "Manual review checklist:",
        "",
        "- Product appears attached near the intended hand/hip area.",
        "- Product does not cover face, torso center, or important hand detail.",
        "- Scale is plausible for a handbag.",
        "- Transparent product layer has no rectangular background.",
        "- Recommended anchor can be copied into action metadata.",
        "",
        "| anchor | output | alpha? | x/y/scale | rendered size | recommended? | notes |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for result in results:
        lines.append(
            f"| {result.anchor_id} | `{result.output_path}` | {result.product_has_alpha} | "
            f"{result.x_ratio}/{result.y_ratio}/{result.scale_ratio} | "
            f"{result.rendered_width}x{result.rendered_height} |  |  |"
        )
    docs_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    recipe = compile_scene_recipe(_load_recipe(args.recipe_file))
    source_dir = _run_source_if_needed(args, recipe.request_hash)
    hero_path = source_dir / "hero_still.png"
    run_id = args.run_id or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_dir = project_root() / "assets/outputs/composite_anchor_tuning" / run_id

    results: list[AnchorTuningResult] = []
    for anchor_id in args.anchors:
        output_path = run_dir / f"product_locked_composite_{anchor_id}.png"
        result = render_product_locked_composite(
            hero_path,
            recipe.product,
            recipe.action,
            output_path,
            anchor_id=anchor_id,
        )
        results.append(
            AnchorTuningResult(
                anchor_id=result.anchor_id,
                output_path=_display(output_path),
                product_has_alpha=result.product_has_alpha,
                product_alpha_bbox=result.product_alpha_bbox,
                x_ratio=result.x_ratio,
                y_ratio=result.y_ratio,
                scale_ratio=result.scale_ratio,
                pixel_x=result.pixel_x,
                pixel_y=result.pixel_y,
                rendered_width=result.rendered_width,
                rendered_height=result.rendered_height,
                notes=result.notes,
            )
        )

    contact_sheet = run_dir / "anchor_contact_sheet.png"
    _make_contact_sheet(results, contact_sheet)
    _write_reports(run_id, args, source_dir, contact_sheet, results)
    print(f"run_id: {run_id}")
    print(f"contact_sheet: {_display(contact_sheet)}")
    print("updated docs/composite_anchor_tuning_results.md")


if __name__ == "__main__":
    main()
