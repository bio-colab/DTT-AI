#!/usr/bin/env python3
"""Fermi Estimation & Order-of-Magnitude Calculator (DTT_1 Session 3).

Computes a Fermi estimate from explicit numerator and denominator factors,
and rounds to the requested order of magnitude (e.g., -3 for nearest thousand).
"""

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Dict, List


def compute_fermi(
    numerators: List[Dict[str, float]],
    denominators: List[Dict[str, float]],
    round_digits: int = -3,
) -> Dict[str, object]:
    num_val = 1.0
    for item in numerators:
        num_val *= float(item["value"])

    den_val = 1.0
    for item in denominators:
        val = float(item["value"])
        if val == 0:
            raise ValueError(f"Denominator factor '{item['name']}' cannot be zero.")
        den_val *= val

    raw = num_val / den_val
    rounded = round(raw, round_digits)
    return {
        "numerator_total": num_val,
        "denominator_total": den_val,
        "raw_estimate": raw,
        "rounded_estimate": rounded,
        "round_digits": round_digits,
        "order_of_magnitude": math.floor(math.log10(abs(raw))) if raw != 0 else 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute Fermi estimate from JSON spec.")
    parser.add_argument("--spec", required=True, help="JSON string or file path with numerators/denominators.")
    parser.add_argument("--round-digits", type=int, default=-3, help="Python round(x, n) second argument.")
    args = parser.parse_args()

    p = Path(args.spec)
    data = json.loads(p.read_text(encoding="utf-8") if p.is_file() else args.spec)
    res = compute_fermi(data.get("numerators", []), data.get("denominators", []), args.round_digits)
    print(json.dumps(res, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
