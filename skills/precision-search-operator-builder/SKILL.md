---
name: precision-search-operator-builder
description: Build high-precision search queries with Google operators, mitigate algorithmic filter bubbles, route computational queries to knowledge engines, and inspect Wikipedia revision histories. Use when the user needs targeted web research, unbiased search comparisons, or encyclopedia reliability checks.
---
# Precision Search Operator Builder

Construct surgical search queries, burst algorithmic filter bubbles, and audit dynamic reference sources.

## When to Use

- The user needs exact, noise-free search queries for research or OSINT.
- The user suspects personalized search results or filter bubbles are skewing their findings.
- The user wants to verify the stability or edit history of a Wikipedia article.

## Procedure

1. Decompose the user's question into required concepts, excluded noise, target domains, and date bounds.
2. Build the query using these exact operators:
   - Use quotes `"exact phrase"` to match words in exact order.
   - Prefix `-word` (no space after hyphen) to exclude unwanted contexts.
   - Use `*` inside quotes as a single-word or phrase wildcard.
   - Use uppercase `OR` between alternative terms.
   - Use `site:domain` (such as `site:ac.uk` or `site:gov`) to restrict sources.
   - Use `YYYY...YYYY` to restrict results to a specific year range.
3. Combine operators into one compact query string.
4. If the topic is controversial or location-sensitive, warn the user about **filter bubbles**.
5. Recommend running the exact query on a non-tracking engine like DuckDuckGo or in a clean session.
6. If the query asks for dynamic calculations, unit comparisons, or structured statistics, route it to a computational engine like WolframAlpha.
7. Note that computational engines fail on ambiguous jokes or non-factual riddles.
8. When checking a Wikipedia article, inspect `View history` and `Revision history statistics`.
9. Check for recent edit spikes, anonymous IP edits, or revert wars before trusting the page.

## Gotchas

- Always write `OR` in uppercase letters. Lowercase `or` is ignored as a stop word.
- The `YYYY...YYYY` operator can match pages that merely mention those years in text. Always verify the actual publication date.
- Wikipedia is a starting point, not a final authority.
