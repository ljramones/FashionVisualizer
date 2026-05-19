import type { CatalogEntry, SceneRecipe } from "../types/catalog";

interface WorkflowInspectorProps {
  recipe: SceneRecipe | null;
  entry: CatalogEntry | null;
}

export default function WorkflowInspector({ recipe, entry }: WorkflowInspectorProps) {
  return (
    <section className="inspector">
      <h3>Workflow Inspector</h3>
      <dl>
        <div>
          <dt>Recipe Hash</dt>
          <dd>{recipe?.request_hash ?? "not compiled"}</dd>
        </div>
        <div>
          <dt>Selected Route</dt>
          <dd>{entry?.route.name ?? recipe?.route_hint ?? "not selected"}</dd>
        </div>
        <div>
          <dt>Prompt</dt>
          <dd>{recipe?.compiled_prompt ?? "Compile a recipe to inspect the prompt."}</dd>
        </div>
        <div>
          <dt>Negative Prompt</dt>
          <dd>{recipe?.negative_prompt ?? "not compiled"}</dd>
        </div>
        <div>
          <dt>Eval Placeholder</dt>
          <dd>{entry?.eval.notes.join(" ") ?? "Generate a stub to inspect evaluation notes."}</dd>
        </div>
      </dl>
    </section>
  );
}
