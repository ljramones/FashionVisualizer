from scripts.probe_image_models import ProbeResult, render_results_markdown


def test_probe_result_markdown_contains_status_and_model() -> None:
    markdown = render_results_markdown(
        [
            ProbeResult(
                model="example/model",
                display_name="Example",
                device="cpu",
                status="fallback_runtime_error",
                duration_seconds=0.12,
                output="assets/outputs/example/hero_still.png",
                fallback_used=True,
                used_real_generation=False,
                dependency_status={"torch_available": True, "diffusers_available": True},
                error_summary="example error",
                notes=["example note"],
            )
        ]
    )

    assert "example/model" in markdown
    assert "fallback_runtime_error" in markdown
    assert "example error" in markdown
