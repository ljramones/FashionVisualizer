from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.config import resolve_project_path, settings
from backend.app.contracts import (
    ActionRef,
    CatalogEntry,
    EvalResult,
    GenerationRequest,
    LocationRef,
    ModelProfile,
    ProductRef,
    SceneRecipe,
    SystemCapabilities,
)
from backend.app.pipeline.handbag_pipeline import run_handbag_pipeline
from backend.app.recipes.scene_recipe_compiler import compile_scene_recipe
from backend.app.registry.asset_registry import (
    load_actions,
    load_catalog,
    load_locations,
    load_models,
    load_products,
)
from backend.app.routing.hardware_probe import get_system_capabilities
from backend.app.routing.model_router import choose_route

app = FastAPI(
    title="LuxFlow AI",
    description="Local-first workflow studio for product-preserving catalog video recipes.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/static/assets",
    StaticFiles(directory=resolve_project_path(settings.assets_dir)),
    name="static-assets",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "luxflow-ai"}


@app.get("/system/capabilities", response_model=SystemCapabilities)
def system_capabilities() -> SystemCapabilities:
    return get_system_capabilities()


@app.get("/catalog")
def catalog() -> dict[str, object]:
    return load_catalog()


@app.get("/assets/products")
def assets_products() -> list[ProductRef]:
    return load_products()


@app.get("/assets/models")
def assets_models() -> list[ModelProfile]:
    return load_models()


@app.get("/assets/locations")
def assets_locations() -> list[LocationRef]:
    return load_locations()


@app.get("/assets/actions")
def assets_actions() -> list[ActionRef]:
    return load_actions()


@app.post("/recipes/compile", response_model=SceneRecipe)
def recipes_compile(request: GenerationRequest) -> SceneRecipe:
    try:
        return compile_scene_recipe(request)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/generate", response_model=CatalogEntry)
def generate(request: GenerationRequest) -> CatalogEntry:
    """Compile, route, and return a stub catalog entry without running ML."""

    try:
        recipe = compile_scene_recipe(request)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    route = choose_route(recipe)
    if route.name == "unsupported_stub":
        return CatalogEntry(
            id=f"unsupported_{recipe.request_hash}",
            product=recipe.product,
            model=recipe.model,
            location=recipe.location,
            action=recipe.action,
            recipe_hash=recipe.request_hash,
            route=route,
            artifacts=[],
            eval=EvalResult(notes=["Unsupported route; no placeholder artifacts were generated."]),
            status="stub",
        )
    return run_handbag_pipeline(recipe)
