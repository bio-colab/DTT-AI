---
name: argument-extraction-words-to-maps
description: Extract structured argument maps from prose, articles, transcripts, or slides using the three-step Words-to-Maps recipe, discourse connector analysis, and the Dialogue Test. Use when the user pastes text and asks to dissect, map, or extract its underlying argument.
---
# Argument Extraction (Words to Maps)

Extract explicit and implicit argument structures from raw text into a validated argument map.

Humans parse stories easily, but they often miss implicit patterns in argumentative prose.

## When to Use

- The user provides an article, essay, transcript, or slide and asks to map its argument.
- The user asks to identify the main claim, premises, and evidence in a text.
- The user wants to separate actual claims from background descriptions or definitions.

## Procedure

1. Read the full text from start to end before extracting any claims.
2. Locate the Main Claim at Level 0.
3. If the Main Claim is explicit, copy or paraphrase the exact concluding statement.
4. If the Main Claim is implicit, infer the author's overall point and state it clearly.
5. Verify that the Main Claim does not support another claim in the text.
6. Scan the text for discourse connectors that signal `SUPPORT` or `OPPOSE` relations.
7. Map connectors using this lookup table:

| Text Pattern | Connector | Relation |
| :--- | :--- | :--- |
| A because B | because | B supports A |
| A therefore B | therefore | A supports B |
| A for example, B | for example | B supports A |
| A. First, B. Second, C. | first, second | B and C support A |
| A but nevertheless B | but nevertheless | A opposes B |
| A. However B. | however | B opposes A |

8. If no connector exists, apply the Dialogue Test between claim A and candidate B.
9. For support, test: `Speaker 1: A. Speaker 2: Why A? Speaker 1: B.`
10. For opposition, test: `Speaker 1: Not A. Speaker 2: Why not A? Speaker 1: B.`
11. Exclude sentences that only define terms, summarize, or describe background without supporting or opposing a claim.
12. Classify multiple claims at the same parent as `Grouped` if falsifying one breaks the link.
13. Classify multiple claims as `Independent` if each claim stands alone.
14. Repeat steps 6 through 13 for Level 2 and deeper levels until no claims remain.
15. Output the map in `MC` / `SUPPORT` / `OPPOSE` shorthand and validate it with `argument-mapping-core`.

## Gotchas

- Always remove connecting words like `however`, `then`, or `therefore` from the extracted claim text.
- Two valid analysts can produce slightly different maps for the same text. Both maps are acceptable if the analyst can defend the reasoning.
- Watch for `If A then B. If B then C.` chains. Group the chain links together under one `SUPPORT` relation.
