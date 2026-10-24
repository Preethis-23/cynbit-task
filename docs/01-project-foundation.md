# Phase 1: Project Foundation

You are building **Cynbit AI Pre-Sales Solution Architect**, a human-in-the-loop assistant that analyzes client project requirements and prepares a technical and commercial assessment.

## Objective

Establish the project structure, configuration, data contracts, and shared utilities before implementing AI features.

## Tasks

1. Inspect the repository and preserve existing work.
2. Choose a simple Python/Streamlit structure.
3. Add configuration through environment variables or a safe settings module.
4. Define typed schemas for requirements, risks, estimates, assumptions, and proposals.
5. Add a sample requirement document and sample project data for local development.
6. Add a clear README with setup and run instructions.

## Constraints

- Do not use real client or company data.
- Keep secrets out of source control.
- Keep the architecture modular so an LLM provider can be replaced later.
- Do not train a production ML model yet.

## Completion criteria

- The application starts locally.
- Sample input and output schemas are documented.
- Configuration errors are clear.
- Later phases can import the shared schemas and utilities.
