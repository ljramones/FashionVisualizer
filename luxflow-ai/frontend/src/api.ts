import type {
  ActionRef,
  CatalogEntry,
  CatalogResponse,
  GenerationRequest,
  LocationRef,
  ModelProfile,
  ProductRef,
  SceneRecipe
} from "./types/catalog";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`);
  if (!response.ok) {
    throw new Error(`GET ${path} failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

async function postJson<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  if (!response.ok) {
    throw new Error(`POST ${path} failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  catalog: () => getJson<CatalogResponse>("/catalog"),
  products: () => getJson<ProductRef[]>("/assets/products"),
  models: () => getJson<ModelProfile[]>("/assets/models"),
  locations: () => getJson<LocationRef[]>("/assets/locations"),
  actions: () => getJson<ActionRef[]>("/assets/actions"),
  compileRecipe: (request: GenerationRequest) => postJson<SceneRecipe>("/recipes/compile", request),
  generateStub: (request: GenerationRequest) => postJson<CatalogEntry>("/generate", request)
};
