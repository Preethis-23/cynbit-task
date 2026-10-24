# Phase 3: Requirement Analysis

Implement the AI requirement-analysis layer for the Cynbit AI Pre-Sales Solution Architect.

## Objective

Convert an unstructured client brief into a structured, reviewable project analysis.

## Required extraction

Extract:

- business objective
- user roles
- functional requirements
- non-functional requirements
- platforms
- integrations
- AI/ML features
- security and compliance needs
- assumptions
- missing or ambiguous information

## AI behavior

1. Use a configurable LLM client.
2. Request strict structured JSON output.
3. Validate the response against the shared schema.
4. Retry once for invalid structured output.
5. Display the original evidence or explanation for important findings.

## Prompt requirements

- Tell the model not to invent requirements.
- Separate facts from assumptions.
- Mark unknown values as unknown.
- Ask focused clarification questions.
- Keep output professional and concise.

## Completion criteria

- A sample brief produces valid structured output.
- Missing information is visible to the user.
- Invalid model output is handled safely.
- The result is editable and ready for Phase 4.
