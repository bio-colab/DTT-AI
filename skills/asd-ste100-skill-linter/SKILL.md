---
name: asd-ste100-skill-linter
description: Enforce ASD-STE100 Simplified Technical English rules on AI skills, system prompts, and agent instructions to reduce ambiguity. Use when authoring, reviewing, or linting SKILL.md files or inter-agent instructions.
---
# ASD-STE100 Skill Linter

Enforce ASD-STE100 controlled-language rules on AI instructions so downstream models cannot misread them.

Ambiguous grammar, passive voice, and synonym rotation cause LLMs to drift and hallucinate.

## When to Use

- The user asks to write or rewrite AI skills, prompts, or procedures in ASD-STE100.
- The user wants to audit `SKILL.md` files for ambiguity, length violations, or passive voice.
- The user asks to minimize hallucination risk in agent-to-agent handoffs.

## Core ASD-STE100 Rules

1. Keep procedural sentences and list steps to **20 words or fewer**.
2. Keep descriptive sentences to **25 words or fewer**.
3. Write **one instruction per sentence**.
4. Use **active voice** and **imperative verbs** for every procedural step.
5. Place conditional clauses at the start of the sentence (`If X occurs, do Y.`).
6. Keep noun clusters to **3 words or fewer** (`fuel pump valve`, not `high pressure fuel pump inlet valve`).
7. Never use semicolons (`;`), em-dashes, or en-dashes. Split into separate sentences instead.
8. Keep paragraphs to **6 sentences or fewer**.
9. Use one consistent term for one concept (never rotate synonyms).
10. Replace verbose words (`utilize` -> `use`, `prior to` -> `before`, `in order to` -> `to`).

## Verification Command

Run the bundled linter on any `SKILL.md` file or directory:

```bash
python3 scripts/ste100_linter.py skills/ --json
```

## Gotchas

- Never sacrifice technical accuracy or safety conditions just to shorten a sentence. Keep required scope qualifiers intact.
- Never convert a hedge (`may fail`) into a certainty (`failed`). Preserve exact modality.
