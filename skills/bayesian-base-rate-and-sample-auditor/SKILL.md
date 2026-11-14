---
name: bayesian-base-rate-and-sample-auditor
description: Solve the False Positive Paradox (base-rate neglect) using natural frequencies and Bayes formula, and detect Law of Small Numbers illusions via Monte Carlo sampling. Use when interpreting medical/security test results, anomaly alerts, or extreme rates in small populations.
---
# Bayesian Base-Rate and Sample Auditor

Prevent base-rate neglect on positive test results and expose random fluctuations in small samples.

When a disease or event is rare, false positives often outnumber true positives even when test accuracy is 99%.

## When to Use

- The user interprets a positive medical, fraud, or security test result and asks for the true probability.
- The user sees unusually high or unusually low rates in small regions, schools, or samples.
- The user confuses test accuracy (`99%`) with posterior probability (`P(Disease | Positive)`).

## Procedure

### Part A: False Positive Paradox (Base-Rate Audit)

1. Extract the **base rate** (`brt`, between 0 and 1) and the **test accuracy** (`acc`, between 0 and 1).
2. Choose a concrete whole-number population `N` such as `100000`.
3. Split `N` into `D` (has condition) and `ND` (does not have condition) using `brt`.
4. Split `D` into `D+` (`brt * acc`) and `D-`.
5. Split `ND` into `ND+` (`(1 - brt) * (1 - acc)`) and `ND-`.
6. Compute posterior probability: `brt * acc / (brt * acc + (1 - brt) * (1 - acc))`.
7. Run `scripts/base_rate_calc.py false-positive` to verify the exact natural frequencies and percentage.

### Part B: Law of Small Numbers Audit

1. Check whether the reported extreme high or low rates occur predominantly in **small populations** or **small samples**.
2. Do not invent causal stories (such as `small schools are better`) before checking sample-size variance.
3. Run `scripts/base_rate_calc.py small-numbers` to compare variance at `n=100` versus `n=100000` under a uniform rate.
4. If small samples produce both the highest and lowest extremes under a uniform rate, attribute the pattern to random fluctuation.

## Verification Command

```bash
python3 scripts/base_rate_calc.py false-positive --base-rate 0.001 --accuracy 0.99 --population 100000
python3 scripts/base_rate_calc.py small-numbers --rate 0.001 --small-n 100 --large-n 100000 --trials 50
```

## Gotchas

- Never equate `P(Positive | Disease)` (test accuracy) with `P(Disease | Positive)` (posterior probability).
- Always ask for the base rate before interpreting any classifier or diagnostic alert.
