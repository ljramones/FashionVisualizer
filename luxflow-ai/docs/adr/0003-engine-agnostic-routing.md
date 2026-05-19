# ADR 0003: Engine-Agnostic Routing

## Status

Accepted

## Context

Future routes may include Diffusers, ComfyUI, LTX, and hosted fallback engines. The public request should not expose internal engine stage configuration.

## Decision

Public requests compile into `SceneRecipe` objects. A router maps recipes and modes to named pipeline routes.

## Consequences

The UI and API remain stable while engine implementations evolve. Route-specific configuration can remain internal.
