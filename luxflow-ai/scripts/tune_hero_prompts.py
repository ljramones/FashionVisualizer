import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from backend.app import config
from backend.app.config import project_root
from backend.app.demo import load_golden_generation_request
from backend.app.generation.prompt_variants import get_prompt_variants
from backend.app.pipeline.handbag_pipeline import run_handbag_pipeline
from backend.app.recipes.scene_recipe_compiler import compile_scene_recipe
from PIL import Image, ImageDraw
from pydantic import BaseModel

DEFAULT_VARIANTS = [
    "strict_empty_hand_no_accessory_v1",
    "studio_safe_pose_v1",
    "minimal_accessory_free_v1",
]
DEFAULT_ACTIONS = ["standing_right_hand_visible"]


class PromptTuningResult(BaseModel):
    action_id: str
    variant_id: str
    seed: int
    status: str
    used_real_generation: bool
    fallback_used: bool
    duration_seconds: float | None
    output_path: str
    trace_path: str
    positive_prompt_preview: str | None
    negative_prompt_preview: str | None
    final_catalog_action_label: str | None
    hero_action_prompt_used: str | None
    forbidden_generated_objects: list[str]
    no_accessory_strategy: bool
    manual_review: dict[str, str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate hero-still prompt tuning contact sheets."
    )
    parser.add_argument("--profile-id", default="sdxl_turbo_preview")
    parser.add_argument("--width", type=int, default=512)
    parser.add_argument("--height", type=int, default=768)
    parser.add_argument("--steps", type=int, default=2)
    parser.add_argument("--guidance-scale", type=float, default=0.0)
    parser.add_argument("--device", choices=["auto", "mps", "cpu", "cuda"], default="auto")
    parser.add_argument("--seeds", type=int, nargs="+", default=[42, 43])
    parser.add_argument("--variants", nargs="+", default=DEFAULT_VARIANTS)
    parser.add_argument("--actions", nargs="+", default=DEFAULT_ACTIONS)
    parser.add_argument("--run-id")
    return parser.parse_args()


def _artifact_path(entry_artifacts: list[Any], kind: str) -> str:
    for artifact in entry_artifacts:
        if artifact.kind == kind:
            return artifact.path
    raise ValueError(f"Missing artifact: {kind}")


def _configure_generation(args: argparse.Namespace, variant_id: str) -> None:
    config.settings.enable_real_image_generation = True
    config.settings.image_generation_backend = "diffusers"
    config.settings.image_profile_id = args.profile_id
    config.settings.image_prompt_variant_id = variant_id
    config.settings.image_width = args.width
    config.settings.image_height = args.height
    config.settings.image_steps = args.steps
    config.settings.image_guidance_scale = args.guidance_scale
    config.settings.image_device = args.device


def _manual_review_template() -> dict[str, str]:
    return {
        "hand_area_usable": "",
        "no_unwanted_accessory": "",
        "model_action_believable": "",
        "scene_matches": "",
        "recommended": "",
    }


def run_variant_seed(
    args: argparse.Namespace,
    run_dir: Path,
    action_id: str,
    variant_id: str,
    seed: int,
) -> PromptTuningResult:
    _configure_generation(args, variant_id)
    request = load_golden_generation_request().model_copy(
        update={"seed": seed, "action_id": action_id}
    )
    recipe = compile_scene_recipe(request)
    output_root = run_dir / action_id / variant_id
    entry = run_handbag_pipeline(recipe, output_root=output_root)
    trace_path = output_root / entry.recipe_hash / "pipeline_trace.json"
    trace = json.loads(trace_path.read_text(encoding="utf-8"))
    hero_generation = trace["hero_still_generation"]
    hero_path = _artifact_path(entry.artifacts, "hero_still")

    return PromptTuningResult(
        action_id=action_id,
        variant_id=variant_id,
        seed=seed,
        status="success_real_generation"
        if hero_generation.get("used_real_generation")
        else "fallback",
        used_real_generation=bool(hero_generation.get("used_real_generation")),
        fallback_used=bool(hero_generation.get("fallback_used")),
        duration_seconds=hero_generation.get("duration_seconds"),
        output_path=hero_path,
        trace_path=trace_path.relative_to(project_root()).as_posix(),
        positive_prompt_preview=hero_generation.get("positive_prompt_preview"),
        negative_prompt_preview=hero_generation.get("negative_prompt_preview"),
        final_catalog_action_label=hero_generation.get("final_catalog_action_label"),
        hero_action_prompt_used=hero_generation.get("hero_action_prompt_used"),
        forbidden_generated_objects=hero_generation.get("forbidden_generated_objects", []),
        no_accessory_strategy=bool(hero_generation.get("no_accessory_strategy")),
        manual_review=_manual_review_template(),
    )


def make_contact_sheet(results: list[PromptTuningResult], contact_sheet_path: Path) -> None:
    thumb_width = 220
    thumb_height = 330
    label_height = 58
    columns = 3
    rows = (len(results) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * thumb_width, rows * (thumb_height + label_height)), "white")
    draw = ImageDraw.Draw(sheet)

    for index, result in enumerate(results):
        source = project_root() / result.output_path
        with Image.open(source) as image:
            image.thumbnail((thumb_width, thumb_height))
            x = (index % columns) * thumb_width
            y = (index // columns) * (thumb_height + label_height)
            sheet.paste(image.convert("RGB"), (x, y))
            draw.text(
                (x + 6, y + thumb_height + 6),
                f"{result.action_id}\n{result.variant_id}\nseed {result.seed} | {result.status}",
                fill=(20, 20, 20),
            )

    contact_sheet_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(contact_sheet_path)


def write_report(
    run_id: str,
    args: argparse.Namespace,
    results: list[PromptTuningResult],
    contact_sheet_path: Path,
) -> None:
    report_path = contact_sheet_path.parent / "prompt_tuning_report.json"
    report = {
        "run_id": run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "profile_id": args.profile_id,
        "width": args.width,
        "height": args.height,
        "steps": args.steps,
        "guidance_scale": args.guidance_scale,
        "seeds": args.seeds,
        "variants": args.variants,
        "actions": args.actions,
        "contact_sheet": contact_sheet_path.relative_to(project_root()).as_posix(),
        "results": [result.model_dump(mode="json") for result in results],
    }
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    docs_path = project_root() / "docs/prompt_tuning_results.md"
    lines = [
        "# Hero-Still Prompt Tuning Results",
        "",
        f"Run ID: `{run_id}`",
        f"Run timestamp: `{report['created_at']}`",
        f"Profile: `{args.profile_id}`",
        f"Image size: `{args.width}x{args.height}`",
        f"Steps: `{args.steps}`",
        f"Seeds: `{', '.join(str(seed) for seed in args.seeds)}`",
        f"Actions: `{', '.join(args.actions)}`",
        f"Contact sheet: `{report['contact_sheet']}`",
        "",
        "Manual review columns are intentionally blank for human scoring.",
        "",
        "Current tuning focus: separate final catalog action from hero-stage action so "
        "the image model produces empty visible hands and clean placement space instead "
        "of hallucinated accessories.",
        "",
        "| action | variant | seed | status | output | hand area usable? | "
        "no unwanted accessory? | "
        "model/action believable? | scene matches? | recommended? |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for result in results:
        lines.append(
            f"| {result.action_id} | {result.variant_id} | {result.seed} | {result.status} | "
            f"`{result.output_path}` |  |  |  |  |  |"
        )
    docs_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    known_variants = {variant.variant_id for variant in get_prompt_variants()}
    unknown = [variant for variant in args.variants if variant not in known_variants]
    if unknown:
        raise ValueError(f"Unknown prompt variants: {', '.join(unknown)}")

    run_id = args.run_id or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_dir = project_root() / "assets/outputs/prompt_tuning" / run_id
    results: list[PromptTuningResult] = []

    for action_id in args.actions:
        for variant_id in args.variants:
            for seed in args.seeds:
                print(f"generating action={action_id} variant={variant_id} seed={seed}")
                results.append(run_variant_seed(args, run_dir, action_id, variant_id, seed))

    contact_sheet_path = run_dir / "contact_sheet.png"
    make_contact_sheet(results, contact_sheet_path)
    write_report(run_id, args, results, contact_sheet_path)
    print(f"run_id: {run_id}")
    print(f"contact_sheet: {contact_sheet_path.relative_to(project_root()).as_posix()}")
    print("updated docs/prompt_tuning_results.md")


if __name__ == "__main__":
    main()
