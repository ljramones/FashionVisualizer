import { useEffect, useMemo, useState } from "react";
import { api } from "../api";
import type {
  ActionRef,
  AspectRatio,
  CatalogEntry,
  GenerationMode,
  GenerationRequest,
  LocationRef,
  ModelProfile,
  ProductRef,
  SceneRecipe
} from "../types/catalog";
import EvalPanel from "./EvalPanel";
import ArtifactPreview from "./ArtifactPreview";
import RecipeViewer from "./RecipeViewer";
import WorkflowInspector from "./WorkflowInspector";

export default function WorkflowMode() {
  const [products, setProducts] = useState<ProductRef[]>([]);
  const [models, setModels] = useState<ModelProfile[]>([]);
  const [locations, setLocations] = useState<LocationRef[]>([]);
  const [actions, setActions] = useState<ActionRef[]>([]);
  const [mode, setMode] = useState<GenerationMode>("preview");
  const [aspectRatio, setAspectRatio] = useState<AspectRatio>("9:16");
  const [seed, setSeed] = useState(42);
  const [recipe, setRecipe] = useState<SceneRecipe | null>(null);
  const [entry, setEntry] = useState<CatalogEntry | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([api.products(), api.models(), api.locations(), api.actions()])
      .then(([productData, modelData, locationData, actionData]) => {
        setProducts(productData);
        setModels(modelData);
        setLocations(locationData);
        setActions(actionData);
      })
      .catch((err: Error) => setError(err.message));
  }, []);

  const [productId, setProductId] = useState("");
  const [modelId, setModelId] = useState("");
  const [locationId, setLocationId] = useState("");
  const [actionId, setActionId] = useState("");

  useEffect(() => {
    if (!productId && products[0]) setProductId(products[0].id);
    if (!modelId && models[0]) setModelId(models[0].id);
    if (!locationId && locations[0]) setLocationId(locations[0].id);
    if (!actionId && actions[0]) setActionId(actions[0].id);
  }, [products, models, locations, actions, productId, modelId, locationId, actionId]);

  const request = useMemo<GenerationRequest>(
    () => ({
      product_id: productId,
      model_id: modelId,
      location_id: locationId,
      action_id: actionId,
      seed,
      aspect_ratio: aspectRatio,
      mode
    }),
    [productId, modelId, locationId, actionId, seed, aspectRatio, mode]
  );

  async function compile() {
    setError(null);
    setEntry(null);
    setRecipe(await api.compileRecipe(request));
  }

  async function generate() {
    setError(null);
    const generated = await api.generateStub(request);
    setEntry(generated);
  }

  return (
    <section className="workflow-layout">
      <form className="control-panel" onSubmit={(event) => event.preventDefault()}>
        <h2>Workflow</h2>
        <Select label="Product" value={productId} onChange={setProductId} options={products.map(toOption)} />
        <Select label="Model" value={modelId} onChange={setModelId} options={models.map((item) => ({ id: item.id, label: item.display_name }))} />
        <Select label="Location" value={locationId} onChange={setLocationId} options={locations.map(toOption)} />
        <Select label="Action" value={actionId} onChange={setActionId} options={actions.map(toOption)} />
        <Select label="Mode" value={mode} onChange={(value) => setMode(value as GenerationMode)} options={["cached", "preview", "quality"].map((value) => ({ id: value, label: value }))} />
        <Select label="Aspect Ratio" value={aspectRatio} onChange={(value) => setAspectRatio(value as AspectRatio)} options={["9:16", "1:1"].map((value) => ({ id: value, label: value }))} />
        <label>
          Seed
          <input type="number" min="0" value={seed} onChange={(event) => setSeed(Number(event.target.value))} />
        </label>
        <div className="button-row">
          <button type="button" onClick={compile} disabled={!productId}>
            Compile Recipe
          </button>
          <button type="button" onClick={generate} disabled={!productId}>
            Generate Stub
          </button>
        </div>
        {error ? <p className="error">{error}</p> : null}
      </form>
      <div className="workflow-results">
        <ArtifactPreview entry={entry} />
        <WorkflowInspector recipe={recipe} entry={entry} />
        <RecipeViewer title="SceneRecipe JSON" data={recipe} />
        <RecipeViewer title="CatalogEntry JSON" data={entry} />
        <EvalPanel evalResult={entry?.eval ?? null} />
      </div>
    </section>
  );
}

function toOption(item: { id: string; name: string }) {
  return { id: item.id, label: item.name };
}

function Select({
  label,
  value,
  onChange,
  options
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  options: { id: string; label: string }[];
}) {
  return (
    <label>
      {label}
      <select value={value} onChange={(event) => onChange(event.target.value)}>
        {options.map((option) => (
          <option key={option.id} value={option.id}>
            {option.label}
          </option>
        ))}
      </select>
    </label>
  );
}
