import { useEffect, useState } from "react";
import { api, resolveBackendUrl } from "../api";
import type { CatalogEntry, PipelineTrace } from "../types/catalog";

interface PipelineTraceViewerProps {
  entry: CatalogEntry | null;
}

export default function PipelineTraceViewer({ entry }: PipelineTraceViewerProps) {
  const [trace, setTrace] = useState<PipelineTrace | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const traceArtifact = entry?.artifacts.find((artifact) => artifact.kind === "pipeline_trace");
    const traceUrl = resolveBackendUrl(traceArtifact?.static_url);
    setTrace(null);
    setError(null);

    if (!traceUrl) {
      return;
    }

    api
      .pipelineTrace(traceUrl)
      .then(setTrace)
      .catch((err: Error) => setError(err.message));
  }, [entry]);

  if (!entry) {
    return null;
  }

  return (
    <section className="trace-viewer">
      <h3>Pipeline Trace</h3>
      {error ? <p className="error">{error}</p> : null}
      {trace ? (
        <>
          <dl>
            <div>
              <dt>Request Hash</dt>
              <dd>{trace.request_hash}</dd>
            </div>
            <div>
              <dt>Route</dt>
              <dd>{trace.route}</dd>
            </div>
            <div>
              <dt>Mode</dt>
              <dd>{trace.mode}</dd>
            </div>
            <div>
              <dt>ML Execution</dt>
              <dd>{String(trace.ml_execution)}</dd>
            </div>
          </dl>
          <ol className="stage-list">
            {trace.stages.map((stage) => (
              <li key={stage.stage_id}>
                <strong>{stage.label}</strong>
                <span>{stage.status}</span>
                <small>{stage.notes.join(" ")}</small>
              </li>
            ))}
          </ol>
          <div className="preservation-box">
            <strong>Hero still generation</strong>
            <span>
              enabled: {String(trace.hero_still_generation.real_generation_enabled)}
            </span>
            <span>attempted: {String(trace.hero_still_generation.generation_attempted)}</span>
            <span>used real generation: {String(trace.hero_still_generation.used_real_generation)}</span>
            <span>profile: {trace.hero_still_generation.profile_id ?? "n/a"}</span>
            <span>
              variant: {trace.hero_still_generation.prompt_variant_id ?? "n/a"}
            </span>
            <span>model: {trace.hero_still_generation.model_id}</span>
            <span>device: {trace.hero_still_generation.device}</span>
            <span>
              size: {trace.hero_still_generation.width ?? "n/a"} x{" "}
              {trace.hero_still_generation.height ?? "n/a"}
            </span>
            <span>steps: {trace.hero_still_generation.steps ?? "n/a"}</span>
            <span>
              guidance: {trace.hero_still_generation.guidance_scale ?? "n/a"}
            </span>
            <span>
              negative prompt:{" "}
              {String(trace.hero_still_generation.supports_negative_prompt ?? false)}
            </span>
            <span>
              strategy: {trace.hero_still_generation.prompt_strategy ?? "n/a"}
            </span>
            <span>
              target: {trace.hero_still_generation.composition_target_summary ?? "n/a"}
            </span>
            <span>fallback used: {String(trace.hero_still_generation.fallback_used)}</span>
            <span>duration: {trace.hero_still_generation.duration_seconds ?? "n/a"}s</span>
            <span>
              deps: torch {String(trace.hero_still_generation.dependency_status.torch_available)}
              , diffusers{" "}
              {String(trace.hero_still_generation.dependency_status.diffusers_available)}
            </span>
            {trace.hero_still_generation.error_summary ? (
              <small>{trace.hero_still_generation.error_summary}</small>
            ) : null}
            {trace.hero_still_generation.positive_prompt_preview ? (
              <small>{trace.hero_still_generation.positive_prompt_preview}</small>
            ) : null}
            {trace.hero_still_generation.negative_prompt_preview ? (
              <small>{trace.hero_still_generation.negative_prompt_preview}</small>
            ) : null}
            <small>{trace.hero_still_generation.notes.join(" ")}</small>
            {trace.hero_still_generation.error ? (
              <small>{trace.hero_still_generation.error}</small>
            ) : null}
          </div>
          <div className="preservation-box">
            <strong>Product preservation</strong>
            <span>
              freeze core pixels: {String(trace.product_preservation.freeze_core_pixels)}
            </span>
            <span>
              destructive diffusion allowed:{" "}
              {String(trace.product_preservation.destructive_diffusion_allowed)}
            </span>
            <small>{trace.product_preservation.notes.join(" ")}</small>
          </div>
          <p className="next-stage">{trace.next_real_stage}</p>
        </>
      ) : (
        <p>Loading trace metadata...</p>
      )}
    </section>
  );
}
