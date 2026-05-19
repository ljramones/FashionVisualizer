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
