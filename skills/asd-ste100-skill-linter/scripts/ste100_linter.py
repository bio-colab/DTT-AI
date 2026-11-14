#!/usr/bin/env python3
"""STE-style Structural & Lexical Linter for AI Skills (SKILL.md).

Checks a SUBSET of ASD-STE100 style rules (structure and a small banned-word list).
It does NOT check the official approved-vocabulary dictionary or word classes, so a
PASS means "STE-style", not formal ASD-STE100 compliance.

Rules checked:
- Sentence length: <= 20 words (procedural/list steps), <= 25 words (descriptive)
- Zero semicolons (Rule 8.1)
- No em-dashes or en-dashes (use hyphens or periods)
- No passive voice heuristics ('is/are/was/were/be/been + past participle')
- No unapproved vague/marketing words or verbose phrases ('utilize', 'leverage', 'in order to', 'prior to')
- Paragraph limit: <= 6 sentences per paragraph
- Valid SKILL.md YAML frontmatter (name, description)
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List


UNAPPROVED_REPLACEMENTS = {
    "utilize": "use",
    "utilise": "use",
    "leverage": "use",
    "commence": "start",
    "terminate": "stop",
    "prior to": "before",
    "subsequent to": "after",
    "in order to": "to",
    "approximately": "about",
    "sufficient": "enough",
    "obtain": "get",
    "ensure": "make sure",
    "verify": "check",
    "synergistic": "(remove marketing buzzword)",
    "holistic": "(remove marketing buzzword)",
    "paradigm": "(remove marketing buzzword)",
    "seamlessly": "(remove marketing adverb)",
    "effortlessly": "(remove marketing adverb)",
}

PASSIVE_REGEX = re.compile(
    r"\b(?:is|are|was|were|be|been|being)\s+(?:[a-z]+ed|made|done|given|taken|shown|seen|found|built|written|sent|kept|set)\b",
    re.IGNORECASE,
)


def strip_frontmatter_and_code(text: str) -> tuple[Dict[str, str], List[tuple[int, str]]]:
    """Extract YAML frontmatter and return (frontmatter_dict, list of (line_no, prose_line))."""
    lines = text.splitlines()
    fm: Dict[str, str] = {}
    start_idx = 0

    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                fm_block = "\n".join(lines[1:i])
                for fm_line in fm_block.splitlines():
                    if ":" in fm_line:
                        k, v = fm_line.split(":", 1)
                        fm[k.strip()] = v.strip().strip("'\"")
                start_idx = i + 1
                break

    prose_lines: List[tuple[int, str]] = []
    in_code = False
    for idx in range(start_idx, len(lines)):
        line = lines[idx]
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        # Skip markdown table separator rows and pure HTML comments
        if re.match(r"^\|[\s:\-\|]+\|$", stripped) or stripped.startswith("<!--"):
            continue
        prose_lines.append((idx + 1, line))
    return fm, prose_lines


def split_sentences(text: str) -> List[str]:
    """Split a block of text into sentences, ignoring decimals and abbreviations."""
    # Remove inline code spans so code syntax doesn't trigger false positives
    cleaned = re.sub(r"`[^`]+`", "CODE_SPAN", text)
    # Remove markdown link URLs, keeping anchor text
    cleaned = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", cleaned)
    parts = re.split(r"(?<=[.!?])\s+", cleaned.strip())
    return [p.strip() for p in parts if p.strip()]


def lint_markdown(path: Path, strict: bool = True) -> Dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    fm, prose_lines = strip_frontmatter_and_code(raw)

    errors: List[Dict[str, Any]] = []
    warnings: List[Dict[str, Any]] = []

    # 1. Frontmatter validation for SKILL.md
    if path.name == "SKILL.md":
        name = fm.get("name", "")
        desc = fm.get("description", "")
        if not name:
            errors.append({"line": 1, "rule": "FRONTMATTER-NAME", "message": "Missing 'name' in YAML frontmatter."})
        elif not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", name) or len(name) > 64:
            errors.append({"line": 1, "rule": "FRONTMATTER-NAME", "message": f"Invalid kebab-case name: '{name}'."})
        if not desc:
            errors.append({"line": 1, "rule": "FRONTMATTER-DESC", "message": "Missing 'description' in YAML frontmatter."})
        elif len(desc) > 1024:
            errors.append({"line": 1, "rule": "FRONTMATTER-DESC", "message": "Description exceeds 1024 characters."})

    # 2. Line-level punctuation & paragraph grouping
    paragraphs: List[tuple[int, List[str]]] = []
    current_para_start = 0
    current_para: List[str] = []

    for line_no, line in prose_lines:
        stripped = line.strip()
        prose_only = re.sub(r"`[^`]*`", "", line)
        if ";" in prose_only:
            errors.append({"line": line_no, "rule": "STE-8.1", "message": "Semicolon detected. Split into separate sentences."})
        if "—" in prose_only or "–" in prose_only:
            errors.append({"line": line_no, "rule": "SKILL-DASH", "message": "Em-dash or en-dash detected. Use hyphen or period."})

        # Treat headings, list items, table rows, blockquotes as standalone units
        if not stripped:
            if current_para:
                paragraphs.append((current_para_start, current_para))
                current_para = []
            continue

        is_list_or_header = bool(re.match(r"^(?:#+|\*|\-|\d+\.|>|\|)\s+", stripped))
        if is_list_or_header:
            if current_para:
                paragraphs.append((current_para_start, current_para))
                current_para = []
            paragraphs.append((line_no, [stripped]))
        else:
            if not current_para:
                current_para_start = line_no
            current_para.append(stripped)

    if current_para:
        paragraphs.append((current_para_start, current_para))

    total_sentences = 0
    for start_line, para_lines in paragraphs:
        block = " ".join(para_lines)
        # Strip leading markdown list/header markers
        is_procedural = bool(re.match(r"^(?:\d+\.|\*|\-)\s+", block))
        clean_block = re.sub(r"^(?:#+\s+|\d+\.\s+|\*\s+|\-\s+|>\s+)", "", block)
        if clean_block.startswith("|"):
            continue  # Skip pipe table rows for sentence length

        sentences = split_sentences(clean_block)
        if len(sentences) > 6:
            warnings.append({
                "line": start_line,
                "rule": "STE-PARA-LEN",
                "message": f"Paragraph has {len(sentences)} sentences (max 6).",
            })

        for sent in sentences:
            total_sentences += 1
            words = re.findall(r"[A-Za-z0-9_'-]+", sent)
            max_words = 20 if is_procedural else 25
            if len(words) > max_words:
                msg = f"Sentence has {len(words)} words (max {max_words}): '{sent[:60]}...'"
                if strict:
                    errors.append({"line": start_line, "rule": "STE-SENT-LEN", "message": msg})
                else:
                    warnings.append({"line": start_line, "rule": "STE-SENT-LEN", "message": msg})

            if PASSIVE_REGEX.search(sent):
                warnings.append({
                    "line": start_line,
                    "rule": "STE-ACTIVE-VOICE",
                    "message": f"Possible passive voice: '{sent[:60]}'",
                })

            lower_sent = sent.lower()
            for bad, good in UNAPPROVED_REPLACEMENTS.items():
                if re.search(rf"\b{re.escape(bad)}\b", lower_sent):
                    warnings.append({
                        "line": start_line,
                        "rule": "STE-VOCAB",
                        "message": f"Replace '{bad}' with '{good}'.",
                    })

    return {
        "file": str(path),
        "passed": len(errors) == 0,
        "total_sentences": total_sentences,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint SKILL.md files for ASD-STE100 compliance.")
    parser.add_argument("paths", nargs="+", help="Files or directories to lint.")
    parser.add_argument("--json", action="store_true", help="Output JSON report.")
    parser.add_argument("--lenient", action="store_true", help="Treat sentence length overages as warnings.")
    args = parser.parse_args()

    targets: List[Path] = []
    for p_str in args.paths:
        p = Path(p_str)
        if p.is_dir():
            targets.extend(sorted(p.rglob("SKILL.md")))
        elif p.is_file():
            targets.append(p)

    if not targets:
        print("No target files found.", file=sys.stderr)
        return 1

    results = [lint_markdown(t, strict=not args.lenient) for t in targets]
    all_passed = all(r["passed"] for r in results)

    if args.json:
        print(json.dumps({"all_passed": all_passed, "results": results}, indent=2))
    else:
        for r in results:
            status = "PASS" if r["passed"] else "FAIL"
            print(f"[{status}] {r['file']} (sentences={r['total_sentences']}, errors={r['error_count']}, warnings={r['warning_count']})")
            for e in r["errors"]:
                print(f"  ERROR L{e['line']} [{e['rule']}]: {e['message']}")
            for w in r["warnings"][:5]:
                print(f"  WARN  L{w['line']} [{w['rule']}]: {w['message']}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
