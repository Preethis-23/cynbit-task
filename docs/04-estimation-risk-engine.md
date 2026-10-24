# Phase 4: Estimation and Risk Engine

Implement transparent effort, cost, timeline, complexity, and risk estimation.

## Objective

Turn the structured requirements into an explainable commercial assessment. The system recommends; Cynbit’s team decides.

## Required calculations

Support configurable values for:

- estimated hours by feature category
- complexity multiplier
- integration effort
- testing and deployment effort
- contingency percentage
- hourly internal cost
- target profit margin

Use formulas such as:

```text
internal_cost = estimated_hours * hourly_internal_cost
expected_profit = quotation_price - internal_cost
profit_margin = expected_profit / quotation_price * 100
```

Return ranges where uncertainty is high.

## Risk scoring

Start with documented rules, for example:

- unclear requirements: +3
- more than two integrations: +2
- web and mobile platforms: +2
- AI feature: +2
- unusually short deadline: +1

Map the total to Low, Medium, or High risk and explain every point.

## Optional ML demonstration

If practical, train a small Random Forest model on clearly labeled synthetic project records for effort or risk prediction. Label this as a demonstration only; do not claim production accuracy.

## Completion criteria

- Calculations are reproducible and visible.
- Assumptions can be edited.
- Risk reasons are understandable.
- No final accept/reject decision is automated.
