#!/usr/bin/env python3
"""Bayesian Base-Rate & Law of Small Numbers Auditor (DTT_1 Session 5).

Implements:
1. False Positive Paradox calculator:
   P(D|+) = (brt * acc) / (brt * acc + (1 - brt) * (1 - acc))
   with natural-frequency breakdown for population N.
2. Law of Small Numbers Monte Carlo simulation comparing small (n=100) vs large (n=100,000) samples.
"""

import argparse
import json
import random
import sys
from typing import Dict


def false_positive_analysis(base_rate: float, accuracy: float, population: int = 100_000) -> Dict[str, object]:
    if not (0.0 <= base_rate <= 1.0):
        raise ValueError("base_rate must be between 0 and 1.")
    if not (0.0 <= accuracy <= 1.0):
        raise ValueError("accuracy must be between 0 and 1.")

    true_pos_prob = base_rate * accuracy
    false_pos_prob = (1.0 - base_rate) * (1.0 - accuracy)
    total_pos_prob = true_pos_prob + false_pos_prob

    posterior = (true_pos_prob / total_pos_prob) if total_pos_prob > 0 else 0.0

    d_count = round(population * base_rate)
    nd_count = population - d_count
    d_pos = round(d_count * accuracy)
    d_neg = d_count - d_pos
    nd_pos = round(nd_count * (1.0 - accuracy))
    nd_neg = nd_count - nd_pos

    return {
        "base_rate": base_rate,
        "accuracy": accuracy,
        "posterior_probability": round(posterior, 6),
        "posterior_percent": round(posterior * 100.0, 2),
        "natural_frequencies": {
            "population": population,
            "D_total": d_count,
            "ND_total": nd_count,
            "D_positive": d_pos,
            "D_negative": d_neg,
            "ND_positive_false_positives": nd_pos,
            "ND_negative": nd_neg,
            "total_positives": d_pos + nd_pos,
        },
        "base_rate_swamped": nd_pos > d_pos,
    }


def small_numbers_simulation(rate: float, small_n: int = 100, large_n: int = 100_000, trials: int = 50, seed: int = 42) -> Dict[str, object]:
    rng = random.Random(seed)
    small_rates = [sum(1 for _ in range(small_n) if rng.random() < rate) / small_n for _ in range(trials)]
    large_rates = [sum(1 for _ in range(large_n) if rng.random() < rate) / large_n for _ in range(trials)]

    return {
        "true_rate": rate,
        "trials": trials,
        "small_sample": {
            "n": small_n,
            "min_observed_rate": min(small_rates),
            "max_observed_rate": max(small_rates),
            "zero_rate_trials": sum(1 for r in small_rates if r == 0.0),
        },
        "large_sample": {
            "n": large_n,
            "min_observed_rate": round(min(large_rates), 6),
            "max_observed_rate": round(max(large_rates), 6),
            "zero_rate_trials": sum(1 for r in large_rates if r == 0.0),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Base-Rate & Law of Small Numbers calculator.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    fp = sub.add_parser("false-positive", help="Compute False Positive Paradox posterior.")
    fp.add_argument("--base-rate", type=float, required=True, help="Disease/event base rate (0..1).")
    fp.add_argument("--accuracy", type=float, required=True, help="Test accuracy (0..1).")
    fp.add_argument("--population", type=int, default=100_000, help="Population size for natural frequencies.")

    sn = sub.add_parser("small-numbers", help="Simulate Law of Small Numbers variance.")
    sn.add_argument("--rate", type=float, default=0.001, help="True underlying rate (0..1).")
    sn.add_argument("--small-n", type=int, default=100)
    sn.add_argument("--large-n", type=int, default=100_000)
    sn.add_argument("--trials", type=int, default=50)
    sn.add_argument("--seed", type=int, default=42)

    args = parser.parse_args()
    if args.cmd == "false-positive":
        res = false_positive_analysis(args.base_rate, args.accuracy, args.population)
    else:
        res = small_numbers_simulation(args.rate, args.small_n, args.large_n, args.trials, args.seed)

    print(json.dumps(res, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
