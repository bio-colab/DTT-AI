#!/usr/bin/env python3
"""Euler Set Reasoning & Conjunction Fallacy Checker (DTT_1 Session 5)."""

import argparse
import json
import sys
from typing import Any, Dict, Set


def analyze_two_sets(universe_size: int, set_a_size: int, set_b_size: int, intersection_size: int) -> Dict[str, Any]:
    if intersection_size > min(set_a_size, set_b_size):
        raise ValueError("Intersection cannot exceed size of either set.")
    only_a = set_a_size - intersection_size
    only_b = set_b_size - intersection_size
    union_size = only_a + only_b + intersection_size
    if union_size > universe_size:
        raise ValueError("Union cannot exceed universe size.")
    neither = universe_size - union_size

    relation = "INTERSECTION"
    if intersection_size == 0:
        relation = "DISJOINT"
    elif intersection_size == set_a_size:
        relation = "A_SUBSET_OF_B"
    elif intersection_size == set_b_size:
        relation = "B_SUBSET_OF_A"

    return {
        "euler_relation": relation,
        "regions": {
            "A_only": only_a,
            "B_only": only_b,
            "A_and_B": intersection_size,
            "neither": neither,
            "union_A_or_B": union_size,
        },
        "probabilities_percent": {
            "P(A)": round(100 * set_a_size / universe_size, 2),
            "P(B)": round(100 * set_b_size / universe_size, 2),
            "P(A_and_B)": round(100 * intersection_size / universe_size, 2),
            "P(A_only)": round(100 * only_a / universe_size, 2),
            "P(neither)": round(100 * neither / universe_size, 2),
        },
        "conjunction_rule_holds": intersection_size <= set_a_size and intersection_size <= set_b_size,
    }


def set_ops(a_items: Set[str], b_items: Set[str]) -> Dict[str, Any]:
    return {
        "A_count": len(a_items),
        "B_count": len(b_items),
        "intersection": sorted(a_items & b_items),
        "union": sorted(a_items | b_items),
        "A_minus_B": sorted(a_items - b_items),
        "B_minus_A": sorted(b_items - a_items),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Euler diagram set & probability analyzer.")
    parser.add_argument("--universe", type=int, required=True)
    parser.add_argument("--a-size", type=int, required=True)
    parser.add_argument("--b-size", type=int, required=True)
    parser.add_argument("--both", type=int, required=True)
    args = parser.parse_args()

    res = analyze_two_sets(args.universe, args.a_size, args.b_size, args.both)
    print(json.dumps(res, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
