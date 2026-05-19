import type { EvalResult } from "../types/catalog";

interface EvalPanelProps {
  evalResult: EvalResult | null;
}

export default function EvalPanel({ evalResult }: EvalPanelProps) {
  return (
    <section className="eval-panel">
      <h3>Evaluation</h3>
      <div className="score-row">
        <span>Prompt adherence</span>
        <strong>{evalResult?.prompt_adherence_score ?? "pending"}</strong>
      </div>
      <div className="score-row">
        <span>Product preservation</span>
        <strong>{evalResult?.product_preservation_score ?? "pending"}</strong>
      </div>
      <ul className="notes">
        {(evalResult?.notes ?? ["Generate a stub to view evaluation notes."]).map((note) => (
          <li key={note}>{note}</li>
        ))}
      </ul>
    </section>
  );
}
