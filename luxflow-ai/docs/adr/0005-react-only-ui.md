# ADR 0005: React-Only UI

## Status

Accepted

## Context

The project needs a portfolio-grade workflow inspector rather than a quick notebook or model demo UI.

## Decision

The MVP UI uses React, Vite, and TypeScript. Gradio and Streamlit are excluded.

## Consequences

The frontend can support catalog browsing and workflow inspection cleanly. More setup is required than a single-file demo, but the architecture remains product-facing.
