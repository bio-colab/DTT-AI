---
name: assumption-and-base-auditor
description: Audit argument map base claims, detect hidden audience-dependent assumptions, check evidence generalisation scope, and evaluate collaborative map bias such as Kialo voting. Use when reviewing an argument map for hidden flaws, unstated beliefs, or weak evidence.
---
# Assumption and Base Auditor

Audit the bottom layer of an argument map and expose unspoken assumptions that control support or opposition relations.

Claims do not exist in a vacuum. The same fact can support or oppose a claim depending on the audience's unspoken beliefs.

## When to Use

- The user asks to critique, stress-test, or audit an argument map or debate.
- The user shares a collaborative argument map from Kialo, AGORA-net, or similar platforms.
- The user asks why two groups interpret the same evidence in opposite ways.

## Procedure

1. Extract all terminal leaf nodes (base claims) using `scripts/argmap_tool.py --format audit`.
2. Classify each base claim into one of three categories:
   - **Common Knowledge**: Uncontroversial facts accepted by both author and audience.
   - **Trustworthy Evidence**: Peer-reviewed studies, official statistics, or verifiable records.
   - **Unverified Assertion**: Opinions or ungrounded claims that require further support.
3. Flag every `Unverified Assertion` as a weak base that threatens the pyramid.
4. For each `Trustworthy Evidence` node, compare the study's actual scope against the parent claim's scope.
5. Flag any over-generalisation in population, geography, sample size, or outcome measure.
6. For each `SUPPORT` or `OPPOSE` link, write down the unspoken assumption required for the link to hold.
7. Test whether reversing the audience flips the relation from `SUPPORT` to `OPPOSE` (the Tor Stinks test).
8. If the map comes from a voting platform like Kialo, separate vote popularity from logical validity.
9. Warn the user if high-voted claims lack base evidence or reflect a filter bubble.

## Example (The Tor Stinks Assumption Flip)

- **Main Claim**: `Tor stinks.`
- **Fact**: `Security agencies cannot de-anonymize all Tor users all the time.`
- **Audience A (Intelligence Agency)**: Hidden assumption is `Anything that blocks tracking threats is bad.` Result: `SUPPORT`.
- **Audience B (Journalist or Activist)**: Hidden assumption is `Privacy from mass surveillance is good.` Result: `OPPOSE`.

## Gotchas

- Never accept a shared argument map uncritically. Always surface the author's hidden assumptions before adopting the conclusion.
- Popularity on a collaborative map measures crowd sentiment, not truth.
