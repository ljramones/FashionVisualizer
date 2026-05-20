import argparse
import json
import subprocess
import sys
from time import perf_counter
from typing import Any

from backend.app import config
from backend.app.config import project_root
from backend.app.demo import load_golden_generation_request
from backend.app.generation.diffusers_hero_still import generation_dependency_status
from backend.app.generation.image_profiles import ImageGenerationProfile, get_image_profiles
from backend.app.pipeline.handbag_pipeline import run_handbag_pipeline
from backend.app.recipes.scene_recipe_compiler import compile_scene_recipe
from pydantic import BaseModel


class ProbeResult(BaseModel):
    profile: str
    model: str
    display_name: str
    device: str
    status: str
    duration_seconds: float
    output: str | None
    fallback_used: bool
    used_real_generation: bool
    width: int | None = None
    height: int | None = None
    steps: int | None = None
    guidance_scale: float | None = None
    prompt_profile_used: str | None = None
    supports_negative_prompt: bool | None = None
    dependency_status: dict[str, object]
    error_summary: str | None = None
    notes: list[str]


def _safe_model_slug(model_id: str) -> str:
    return model_id.replace("/", "__").replace(":", "_")


def _artifact_path(entry_artifacts: list[Any], kind: str) -> str | None:
    for artifact in entry_artifacts:
        if artifact.kind == kind:
            return artifact.path
    return None


def _status_from_trace(hero_generation: dict[str, Any]) -> str:
    if hero_generation.get("used_real_generation") is True:
        return "success_real_generation"

    error = str(hero_generation.get("error") or hero_generation.get("error_summary") or "").lower()
    if "gated repo" in error or "401 client error" in error or "access is restricted" in error:
        return "fallback_gated_model_access"
    if "not installed" in error or "no module named" in error:
        return "fallback_missing_dependencies"
    return "fallback_runtime_error"


def _apply_profile_settings(profile: ImageGenerationProfile, device: str) -> None:
    config.settings.enable_real_image_generation = True
    config.settings.image_generation_backend = "diffusers"
    config.settings.image_profile_id = profile.profile_id
    config.settings.image_model_id = profile.model_id
    config.settings.image_width = 1024
    config.settings.image_height = 1024
    config.settings.image_steps = 4
    config.settings.image_guidance_scale = 0.0
    config.settings.image_device = device


def probe_profile(profile: ImageGenerationProfile, device: str = "auto") -> ProbeResult:
    _apply_profile_settings(profile, device)
    recipe = compile_scene_recipe(load_golden_generation_request())
    output_root = (
        project_root()
        / "assets/outputs/model_probe"
        / _safe_model_slug(profile.profile_id)
    )

    started = perf_counter()
    entry = run_handbag_pipeline(recipe, output_root=output_root)
    elapsed = round(perf_counter() - started, 3)

    output_dir = output_root / entry.recipe_hash
    trace_path = output_dir / "pipeline_trace.json"
    trace = json.loads(trace_path.read_text(encoding="utf-8"))
    hero_generation = trace["hero_still_generation"]
    output_path = _artifact_path(entry.artifacts, "hero_still")

    notes = [
        *profile.license_note.splitlines(),
        profile.access_note,
        *hero_generation.get("notes", []),
    ]

    return ProbeResult(
        profile=profile.profile_id,
        model=str(hero_generation.get("model_id", profile.model_id)),
        display_name=profile.profile_id,
        device=str(hero_generation.get("device", "unknown")),
        status=_status_from_trace(hero_generation),
        duration_seconds=float(hero_generation.get("duration_seconds") or elapsed),
        output=output_path,
        fallback_used=bool(hero_generation.get("fallback_used")),
        used_real_generation=bool(hero_generation.get("used_real_generation")),
        width=hero_generation.get("width"),
        height=hero_generation.get("height"),
        steps=hero_generation.get("steps"),
        guidance_scale=hero_generation.get("guidance_scale"),
        prompt_profile_used=hero_generation.get("prompt_profile_used"),
        supports_negative_prompt=hero_generation.get("supports_negative_prompt"),
        dependency_status=hero_generation.get("dependency_status", generation_dependency_status()),
        error_summary=hero_generation.get("error_summary"),
        notes=notes,
    )


def _failed_subprocess_result(
    profile: ImageGenerationProfile,
    device: str,
    elapsed: float,
    output: str,
    retry_note: str | None = None,
) -> ProbeResult:
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    summary = next((line for line in reversed(lines) if "failed assertion" in line.lower()), None)
    if summary is None:
        summary = next((line for line in reversed(lines) if "mps" in line.lower()), None)
    if summary is None:
        summary = next((line for line in reversed(lines) if "error" in line.lower()), None)
    if summary is None:
        summary = lines[-1] if lines else "Probe process exited before returning a result."

    notes = [profile.license_note, profile.access_note]
    if retry_note:
        notes.append(retry_note)
        notes.append(
            "Probe subprocess failed; generation fallback could not complete in that process."
        )

    return ProbeResult(
        profile=profile.profile_id,
        model=profile.model_id,
        display_name=profile.profile_id,
        device=device,
        status="fallback_runtime_error",
        duration_seconds=round(elapsed, 3),
        output=None,
        fallback_used=True,
        used_real_generation=False,
        dependency_status=generation_dependency_status(),
        error_summary=summary[:300],
        notes=notes,
    )


def _parse_child_result(output: str) -> ProbeResult | None:
    marker = "__LUXFLOW_PROBE_RESULT__"
    for line in reversed(output.splitlines()):
        if line.startswith(marker):
            return ProbeResult.model_validate_json(line.removeprefix(marker))
    return None


def run_candidate_subprocess(
    profile: ImageGenerationProfile,
    device: str = "auto",
    retry_note: str | None = None,
    timeout_seconds: int = 900,
) -> ProbeResult:
    command = [
        sys.executable,
        __file__,
        "--probe-one",
        profile.profile_id,
        "--device",
        device,
    ]
    started = perf_counter()
    try:
        completed = subprocess.run(  # noqa: S603 - command uses current interpreter and script path.
            command,
            cwd=project_root(),
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
        elapsed = perf_counter() - started
    except subprocess.TimeoutExpired as exc:
        output = f"{exc.stdout or ''}\n{exc.stderr or ''}\nTimed out after {timeout_seconds}s."
        return _failed_subprocess_result(profile, device, timeout_seconds, output, retry_note)

    output = f"{completed.stdout}\n{completed.stderr}"
    parsed = _parse_child_result(output)
    if parsed is not None:
        if retry_note:
            parsed.notes.append(retry_note)
        return parsed
    return _failed_subprocess_result(profile, device, elapsed, output, retry_note)


def probe_profile_isolated(profile: ImageGenerationProfile) -> ProbeResult:
    result = run_candidate_subprocess(profile, device="auto")
    if (
        result.status == "fallback_runtime_error"
        and result.device in {"auto", "mps"}
        and "mps" in str(result.error_summary).lower()
    ):
        return run_candidate_subprocess(
            profile,
            device="cpu",
            retry_note="Auto/MPS probe failed; retried on CPU for smoke validation.",
        )
    return result


def render_results_markdown(results: list[ProbeResult]) -> str:
    lines = [
        "# Image Model Probe Results",
        "",
        "This file is generated by `python scripts/probe_image_models.py`. It records "
        "local model-access behavior for the golden recipe without committing generated outputs.",
        "",
        "| profile | model | device | status | width | height | steps | guidance | "
        "output | fallback used | notes |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for result in results:
        notes = " ".join(result.notes)
        if result.error_summary:
            notes = f"{notes} Error: {result.error_summary}"
        lines.append(
            "| "
            f"{result.profile} | "
            f"{result.model} | "
            f"{result.device} | "
            f"{result.status} | "
            f"{result.width or 'n/a'} | "
            f"{result.height or 'n/a'} | "
            f"{result.steps or 'n/a'} | "
            f"{result.guidance_scale if result.guidance_scale is not None else 'n/a'} | "
            f"{result.output or 'n/a'} | "
            f"{result.fallback_used} | "
            f"{result.duration_seconds:.3f}s. {notes} |"
        )
    return "\n".join(lines) + "\n"


def render_benchmark_section(results: list[ProbeResult]) -> str:
    lines = [
        "## Image Model Probe Results",
        "",
        "| profile | model | device | status | duration | width | height | steps | "
        "guidance_scale | prompt_profile_used | supports_negative_prompt | output | "
        "fallback used | notes |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for result in results:
        notes = result.error_summary or "See docs/model_probe_results.md for full notes."
        lines.append(
            "| "
            f"{result.profile} | "
            f"{result.model} | "
            f"{result.device} | "
            f"{result.status} | "
            f"{result.duration_seconds:.3f}s | "
            f"{result.width or 'n/a'} | "
            f"{result.height or 'n/a'} | "
            f"{result.steps or 'n/a'} | "
            f"{result.guidance_scale if result.guidance_scale is not None else 'n/a'} | "
            f"{result.prompt_profile_used or 'n/a'} | "
            f"{result.supports_negative_prompt} | "
            f"{result.output or 'n/a'} | "
            f"{result.fallback_used} | "
            f"{notes} |"
        )
    return "\n".join(lines) + "\n"


def update_benchmark_results(results: list[ProbeResult]) -> None:
    benchmark_path = project_root() / "docs/benchmark_results.md"
    marker = "\n## Image Model Probe Results\n"
    existing = benchmark_path.read_text(encoding="utf-8") if benchmark_path.exists() else ""
    base = existing.split(marker, maxsplit=1)[0].rstrip()
    benchmark_path.write_text(
        f"{base}\n\n{render_benchmark_section(results)}",
        encoding="utf-8",
    )


def write_probe_outputs(results: list[ProbeResult]) -> None:
    docs_path = project_root() / "docs/model_probe_results.md"
    docs_path.write_text(render_results_markdown(results), encoding="utf-8")

    json_path = project_root() / "assets/outputs/model_probe_results.json"
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps([result.model_dump(mode="json") for result in results], indent=2),
        encoding="utf-8",
    )
    update_benchmark_results(results)


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe configured Diffusers image models.")
    parser.add_argument("--probe-one", help=argparse.SUPPRESS)
    parser.add_argument("--device", default="auto", choices=["auto", "mps", "cpu", "cuda"])
    args = parser.parse_args()

    if args.probe_one:
        profile = next(
            profile
            for profile in get_image_profiles()
            if profile.profile_id == args.probe_one or profile.model_id == args.probe_one
        )
        result = probe_profile(profile, device=args.device)
        print(f"__LUXFLOW_PROBE_RESULT__{result.model_dump_json()}")
        return

    results: list[ProbeResult] = []
    print("LuxFlow AI image model probe")
    print(f"dependencies: {generation_dependency_status()}")
    for profile in get_image_profiles():
        print(f"probing: {profile.profile_id} ({profile.model_id})")
        result = probe_profile_isolated(profile)
        results.append(result)
        print(
            f"  status={result.status} device={result.device} "
            f"duration={result.duration_seconds:.3f}s fallback={result.fallback_used}"
        )

    write_probe_outputs(results)
    print("wrote docs/model_probe_results.md")
    print("updated docs/benchmark_results.md")
    print("wrote assets/outputs/model_probe_results.json")


if __name__ == "__main__":
    main()
