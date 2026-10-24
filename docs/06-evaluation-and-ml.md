# Phase 6: Evaluation and ML Validation

Evaluate the prototype honestly and document what can and cannot be claimed.

## Objective

Measure extraction quality, estimation usefulness, risk detection, and user value without pretending synthetic data represents Cynbit’s real performance.

## Evaluation dataset

Create a small, clearly labeled set of synthetic project briefs covering:

- simple web projects
- mobile and web projects
- payment and third-party integrations
- AI-enabled projects
- incomplete or ambiguous briefs
- unrealistic deadlines

Keep the dataset separate from application code.

## Metrics

Measure:

- required-field extraction accuracy
- missing-requirement detection rate
- risk classification accuracy on labeled examples
- effort prediction error for synthetic examples
- proposal completeness
- response time
- reviewer approval or edit rate

## Required analysis

- Explain that 100–150 real projects may be insufficient for a complex custom model.
- Treat the Random Forest model as a baseline demonstration only.
- Explain that real production training requires estimated and actual project outcomes.
- Identify hallucination, bias, data leakage, and uncertainty risks.

## Completion criteria

- A repeatable evaluation script or notebook exists.
- Results are documented with limitations.
- The report distinguishes rules, LLM inference, embeddings, and custom ML.
