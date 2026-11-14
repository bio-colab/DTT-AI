---
name: fermi-estimation-calculator
description: Solve estimation and sanity-check problems using the Fermi method, explicit assumptions, order-of-magnitude rounding, System 2 decomposition, and Availability Heuristic checks. Use when estimating unknown quantities with limited data or debunking viral numerical claims.
---
# Fermi Estimation Calculator

Generate defensible ballpark estimates from minimal data and audit intuitive guesses against System 1 biases.

## When to Use

- The user asks to estimate an unknown quantity (population, market size, capacity, time) without exact data.
- The user wants to sanity-check a viral numerical claim (such as fitting all humans on one island).
- The user's intuitive guess may be skewed by dramatic news or personal experience.

## Procedure

1. Identify whether the user's question is a **Target Question** requiring slow **System 2** analysis.
2. Check if intuition is substituting an easy **Heuristic Question** (such as **Availability**).
3. Watch for the four Availability triggers: dramatic/frightening, recent news, frequent media coverage, or personal familiarity.
4. Decompose the Target Question into a chain of simple, estimable factors.
5. List every assumption explicitly with its unit and reasonable ballpark value.
6. Separate factors into `numerators` and `denominators`.
7. Execute `scripts/fermi_calc.py` (or Python with `e`-notation such as `65e6`) to compute the raw result.
8. Round the result to an honest order of magnitude using `round(value, -k)` (for example, `-3` for nearest thousand).
9. Do not report false precision (never mix rough estimates with exact small offsets like `100 million and 5 years`).
10. Compare the Fermi estimate against known crowd averages or official benchmarks when available.

## Verification Command

```bash
python3 scripts/fermi_calc.py --spec '{"numerators":[{"name":"uk_pop","value":65e6},{"name":"visits_per_yr","value":3},{"name":"mins_per_visit","value":10}],"denominators":[{"name":"gp_hrs_wk","value":20},{"name":"gp_wks_yr","value":44},{"name":"mins_per_hr","value":60}]}' --round-digits -3
```

## Gotchas

- Never claim exactness for a Fermi estimate. State the assumptions clearly so the user can adjust any factor.
- Remember that **Wisdom of Crowds** improves accuracy only when individual estimates are independent.
