# Repository Guidelines

## Project Structure & Module Organization

This repository is currently empty aside from this guide. As the project grows, keep runtime code, tests, and assets separated clearly:

- `src/`: application source code and reusable modules.
- `tests/`: automated tests mirroring `src/` paths where practical.
- `assets/`: static media, model inputs, sample images, or other non-code resources.
- `docs/`: design notes, setup details, and longer documentation.

Prefer small, purpose-named modules. For example, place visualization logic in `src/visualizer/` and data-loading utilities in `src/data/`.

## Build, Test, and Development Commands

No package manifest or build system is present yet. When adding one, document the canonical commands here and keep them runnable from the root. Examples:

- `npm run dev`: start a local development server for a frontend app.
- `npm test`: run the full test suite.
- `python -m pytest`: run Python tests if the project uses Python.
- `make build`: produce production-ready build artifacts.

Avoid adding duplicate command paths for the same task unless they serve distinct workflows.

## Coding Style & Naming Conventions

Follow the conventions of the primary language introduced to the repository. Until tooling is added, use 2-space indentation for JavaScript, TypeScript, JSON, YAML, and Markdown; use 4-space indentation for Python. Name files descriptively, using `kebab-case` for frontend files and `snake_case.py` for Python modules.

Add formatters and linters early, then make them part of the documented workflow. Common choices include Prettier and ESLint for JavaScript/TypeScript, or Black and Ruff for Python.

## Testing Guidelines

Add tests with the first meaningful implementation, not after the project becomes large. Keep test names behavior-focused, such as `renders_upload_preview` or `loads_supported_image_formats`. Mirror source layout where possible, for example `tests/visualizer/test_renderer.py` for `src/visualizer/renderer.py`.

Document required fixtures and keep large binary test assets out of the default test path unless they are essential.

## Commit & Pull Request Guidelines

This directory is not currently a Git repository, so no local commit history is available. Use concise, imperative commit messages such as `Add image upload preview` or `Fix renderer scaling`.

Pull requests should include a short description, testing performed, linked issue or task when applicable, and screenshots or screen recordings for visual changes. Call out new dependencies, data files, or configuration changes explicitly.

## Security & Configuration Tips

Do not commit secrets, API keys, model credentials, or local environment files. Use `.env.example` to document required variables and keep real values in untracked local files.
