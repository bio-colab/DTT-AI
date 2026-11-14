---
name: ai-epistemic-and-logic-auditor
description: Audit AI systems, predictions, and technological claims using Rationalist vs Empiricist failure modes, Gödel/Turing/complexity limits, data bias and opacity checks, self-contradiction tests, and the Arendt human-responsibility principle. Use when evaluating AI outputs, algorithmic decisions, or AI-determinism arguments.
---
# AI Epistemic and Logic Auditor

Evaluate AI capabilities, algorithmic risks, and philosophical claims about outsourcing human thinking to machines.

## When to Use

- The user asks whether an AI system or automated algorithm can be trusted for a high-stakes decision.
- The user shares an argument claiming AI will inevitably replace all human judgment.
- The user wants to diagnose why an AI model failed unexpectedly on real-world data.

## Procedure

1. Classify the AI system's underlying approach as **Rationalist** or **Empiricist**:
   - **Rationalist (Axiomatic / Symbolic)**: Derives conclusions from explicit axioms and logic rules (such as Leibniz, Automath, CYC).
   - **Empiricist (Data-Driven / Neural)**: Learns statistical patterns from labeled datasets and user behavior.
2. If the system is **Rationalist**, audit for three known limits:
   - **Gödel-Turing Limit**: No general program can decide truth for all arbitrary statements.
   - **Commonsense Bottleneck**: Everyday knowledge is vast and rarely stated explicitly.
   - **Complexity Explosion**: Even propositional logic becomes computationally infeasible as input facts grow.
   - Distinguish **Proof Discovery** (hard/unsolvable in general) from **Proof Checking** (feasible assistant role).
3. If the system is **Empiricist**, audit for three known failure modes:
   - **Bias in Data**: Training on search logs, user clicks, or human labels encodes societal prejudice.
   - **Algorithmic Opacity**: Black-box neural networks lack transparent step-by-step justification.
   - **Adversarial Brittleness**: Small input changes can flip unrelated labels (the Elephant-in-the-Room effect).
4. Check technological determinism claims for **Self-Contradiction** (the Harari test):
   - Flag any argument that claims humans lack free will while simultaneously urging readers to change the future.
5. Check business incentives behind AI deployment (competitive advantage, cost reduction, ad-engagement maximization) rather than assuming pure benevolence.
6. Apply the **Arendt Responsibility Principle**:
   - Treat AI strictly as a **thinking tool** that assists human reasoning, never as an autonomous moral or decision authority.
   - Keep final judgment and ethical responsibility with the human decision maker.

## Gotchas

- Do not assume that high benchmark accuracy guarantees robustness against out-of-context inputs.
- Never outsource critical ethical or legal judgment to an opaque statistical model.
