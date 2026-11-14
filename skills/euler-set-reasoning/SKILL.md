---
name: euler-set-reasoning
description: Solve categorical logic puzzles (Lewis Carroll syllogisms), set operations (union, intersection, cardinality), and probability partitioning using Euler diagrams instead of Venn diagrams, preventing the Conjunction Fallacy. Use when reasoning about subsets, overlaps, or compound probabilities.
---
# Euler Set Reasoning

Model sets, categorical syllogisms, and compound probabilities using Euler diagrams and Python set operations.

Every region in an Euler diagram represents a non-empty set, unlike Venn diagrams that draw empty overlaps.

## When to Use

- The user asks to solve a categorical logic puzzle (for example, `All A are B. No B are C.`).
- The user compares probabilities of single events versus compound events (the Linda Conjunction Fallacy).
- The user needs exact counts or probabilities across overlapping categories.

## Procedure

1. Define the Universal Set (the outer rectangle containing all items in scope).
2. Identify each distinct class or property as a set (unordered, no duplicate members).
3. Translate each premise into one of three **Euler relations**:
   - **Inclusion**: Set A lies completely inside Set B (`All A are B`).
   - **Disjoint**: Set A and Set B have zero overlap (`No A are B`).
   - **Intersection**: Set A and Set B share some members (`Some A are B`).
4. Check for transitive exclusions across nested ovals. If A is inside B and B is disjoint from C, A is disjoint from C.
5. When checking compound probabilities (`P(A and B)` vs `P(A)`), draw the subset relationship first.
6. Check that `A and B` is a subset of `A`, so `P(A and B)` can never exceed `P(A)`.
7. For numerical set partitioning, run `scripts/euler_sets.py` to compute `A_only`, `B_only`, `A_and_B`, and `neither`.
8. In Python code, use `&` for intersection, `|` for union, and `len()` for cardinality.

## Verification Command

```bash
python3 scripts/euler_sets.py --universe 52 --a-size 12 --b-size 13 --both 3
```

## Gotchas

- Never use a Venn diagram when you want to show that an intersection is empty. Use an Euler diagram with non-overlapping ovals.
- Never let a vivid narrative (System 1 representativeness) trick you into ranking a subset higher than its superset.
