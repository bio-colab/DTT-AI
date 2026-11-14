---
name: argument-mapping-core
description: Build, validate, audit, and export hierarchical argument maps using Level 0-N structure, text shorthand, FreeMind XML, Mermaid, and Argdown. Use when the user asks to create an argument map, structure claims and evidence, visualize pro/con reasoning, or convert argument maps between formats.
---
# Argument Mapping Core

Construct hierarchical argument maps that expose the logical structure of claims, relations, and evidence.

This skill uses ASD-STE100 rules to prevent hallucination and structural drift.

## When to Use

- The user asks to build an argument map for a claim, proposal, or debate.
- The user wants to organize supporting and opposing claims into levels.
- The user asks to export an argument map to FreeMind, Mermaid, Argdown, or JSON.
- The user wants to audit whether an argument has a solid base.

## Core Definitions

- **Main Claim (MC)**: The single central proposition at Level 0.
- **Support Claim (`SUPPORT`)**: A claim that gives a reason to accept its parent claim.
- **Oppose Claim (`OPPOSE`)**: A claim that gives a reason to reject its parent claim.
- **Grouped Claims**: Two or more claims that work together under one relation.
- **Independent Claims**: Separate claims that each stand alone under their own relation.
- **Base Claims**: Terminal leaf claims at the bottom of the tipped-over pyramid.

## Procedure

1. Identify one Main Claim and place it at Level 0.
2. Verify that the Main Claim does not support any other claim in the map.
3. Add at least one Level 1 `SUPPORT` or `OPPOSE` claim.
4. Note that a Main Claim alone is not an argument.
5. Group co-dependent claims under one `SUPPORT` or `OPPOSE` relation.
6. Give each independent claim its own separate `SUPPORT` or `OPPOSE` relation.
7. Add Level 2 and deeper claims until every branch reaches a solid base.
8. Strip discourse connectors such as `however` or `therefore` from claim text.
9. Format the map in canonical shorthand notation.
10. Run `scripts/argmap_tool.py` to validate the structure and export the requested format.

## Canonical Shorthand Format

Use this exact syntax so `scripts/argmap_tool.py` can parse the map:

```text
MC 'Eating carrots improves eyesight.'
SUPPORT 1 'Carrots are a source of Vitamin A.' 2 'Taking vitamin A reduces poor vision risk in deficient individuals.'
SUPPORT 2.1 'Christian et al. (1998) found lower night blindness risk in Asian women given vitamin A.'
OPPOSE 3 'Carrots are a source of beta carotene.' 4 'Beta carotene supplements do not strengthen eyesight in healthy people.'
SUPPORT 4.1 'Christen et al. (2003) found no cataract reduction in healthy US male physicians.'
```

## Verification Command

Run the bundled engine to audit and export the map:

```bash
python3 scripts/argmap_tool.py --input map.txt --format audit
python3 scripts/argmap_tool.py --input map.txt --format mermaid
python3 scripts/argmap_tool.py --input map.txt --format freemind --output map.mm
```

## Gotchas

- Never mix Mind Maps with Argument Maps. Mind Maps link concepts by association, but Argument Maps link claims by `SUPPORT` or `OPPOSE`.
- Never invent citations or study statistics to fill a base node. If evidence is missing, mark the node as unverified.
- If a claim branch has no opposing claims, warn the user that the map lacks balance.
