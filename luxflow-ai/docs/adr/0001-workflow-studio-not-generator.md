# ADR 0001: Workflow Studio, Not Generator

## Status

Accepted

## Context

The first repository pass must demonstrate architecture without downloading weights, calling paid APIs, or executing generation engines.

## Decision

LuxFlow AI will start as a workflow studio with contracts, metadata, routing, documentation, and inspector UI. Generation routes remain stubs.

## Consequences

The repo is lightweight and reviewable. Real generation quality cannot be demonstrated until later passes.
