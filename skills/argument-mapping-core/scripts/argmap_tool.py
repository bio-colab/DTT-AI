#!/usr/bin/env python3
"""Argument Mapping Engine (Open University DTT_1 Sessions 4, 6, 7).

Supports:
- Parsing course shorthand notation:
  MC 'Main claim text.'
  SUPPORT 1 'Claim 1.' 2 'Claim 2.'
  OPPOSE 2.1 'Opposing claim.'
- Validating argument structure (Level 0..N hierarchy, grouped vs independent claims)
- Auditing the Tipped-Over Pyramid Base (identifying terminal base claims)
- Exporting to FreeMind (.mm XML), Mermaid (graph LR), Argdown, and JSON.
"""

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class ClaimNode:
    id: str
    text: str
    level: int
    relation: Optional[str] = None  # None for MC, 'SUPPORT' or 'OPPOSE'
    parent_id: Optional[str] = None
    group_id: Optional[str] = None  # Non-None when multiple claims are grouped under one relation
    children: List[str] = field(default_factory=list)


def parse_shorthand(text: str) -> Dict[str, ClaimNode]:
    """Parse OpenLearn DTT_1 text shorthand into a validated ClaimNode dictionary."""
    nodes: Dict[str, ClaimNode] = {}

    # Normalize whitespace
    clean = " ".join(line.strip() for line in text.strip().splitlines() if line.strip())

    # Extract Main Claim
    mc_match = re.search(r"\bMC\s+['\"]([^'\"]+)['\"]", clean)
    if not mc_match:
        raise ValueError("Missing Main Claim: expected MC '...'")

    nodes["0"] = ClaimNode(id="0", text=mc_match.group(1).strip(), level=0)

    # Find all relation blocks: SUPPORT or OPPOSE followed by one or more <id> '<text>'
    rel_pattern = re.compile(r"\b(SUPPORT|OPPOSE)\b(.*?)(?=\b(?:SUPPORT|OPPOSE)\b|$)")
    claim_pattern = re.compile(r"(\d+(?:\.\d+)*)\s+['\"]([^'\"]+)['\"]")

    rest = clean[mc_match.end():].strip()
    group_counter = 0

    for rel_match in rel_pattern.finditer(rest):
        rel_type = rel_match.group(1)
        body = rel_match.group(2).strip()
        claims = claim_pattern.findall(body)
        if not claims:
            raise ValueError(f"Relation {rel_type} has no valid '<id> \"claim\"' pairs: {body}")

        is_grouped = len(claims) > 1
        grp_id = f"grp_{group_counter}" if is_grouped else None
        if is_grouped:
            group_counter += 1

        for cid, ctext in claims:
            if cid in nodes:
                raise ValueError(f"Duplicate claim ID: {cid}")

            parts = cid.split(".")
            level = len(parts)
            parent_id = "0" if level == 1 else ".".join(parts[:-1])
            if parent_id not in nodes:
                raise ValueError(f"Orphan claim '{cid}': parent '{parent_id}' not defined before child.")

            node = ClaimNode(
                id=cid,
                text=ctext.strip(),
                level=level,
                relation=rel_type,
                parent_id=parent_id,
                group_id=grp_id,
            )
            nodes[cid] = node
            nodes[parent_id].children.append(cid)

    return nodes


def audit_map(nodes: Dict[str, ClaimNode]) -> Dict[str, object]:
    """Audit argument map structure and identify base claims (tipped-over pyramid)."""
    base_claims = [n for n in nodes.values() if len(n.children) == 0 and n.id != "0"]
    support_count = sum(1 for n in nodes.values() if n.relation == "SUPPORT")
    oppose_count = sum(1 for n in nodes.values() if n.relation == "OPPOSE")
    max_level = max((n.level for n in nodes.values()), default=0)
    groups = sorted({n.group_id for n in nodes.values() if n.group_id})

    warnings: List[str] = []
    if len(nodes) == 1:
        warnings.append("Main claim has no supporting or opposing claims. A single claim is not an argument.")
    if oppose_count == 0 and len(nodes) > 1:
        warnings.append("Map has zero opposing claims. Consider counter-arguments for balance.")

    return {
        "valid": len(nodes) > 1,
        "total_claims": len(nodes),
        "max_level": max_level,
        "support_claims": support_count,
        "oppose_claims": oppose_count,
        "grouped_sets_count": len(groups),
        "base_claims": [{"id": n.id, "relation": n.relation, "text": n.text} for n in base_claims],
        "warnings": warnings,
    }


def to_mermaid(nodes: Dict[str, ClaimNode]) -> str:
    """Export argument map to Mermaid flowchart."""
    lines = ["graph LR"]
    for nid, node in nodes.items():
        safe_text = node.text.replace('"', "'")
        if nid == "0":
            lines.append(f'    N0(["MC: {safe_text}"])')
        else:
            safe_id = "N" + nid.replace(".", "_")
            lines.append(f'    {safe_id}["{nid}: {safe_text}"]')

    for nid, node in nodes.items():
        if nid == "0":
            continue
        parent_safe = "N" + node.parent_id.replace(".", "_")
        child_safe = "N" + nid.replace(".", "_")
        label = node.relation or "LINK"
        if node.group_id:
            label = f"{label} ({node.group_id})"
        lines.append(f"    {child_safe} -->|{label}| {parent_safe}")
    return "\n".join(lines)


def to_freemind_xml(nodes: Dict[str, ClaimNode]) -> str:
    """Export argument map to FreeMind (.mm) XML format."""
    root_el = ET.Element("map", version="1.0.1")

    def build_node(parent_el: ET.Element, node: ClaimNode) -> None:
        attrs = {"TEXT": node.text}
        if node.id == "0":
            attrs["STYLE"] = "bubble"
        node_el = ET.SubElement(parent_el, "node", **attrs)
        if node.relation == "SUPPORT":
            ET.SubElement(node_el, "icon", builtin="button_ok")
        elif node.relation == "OPPOSE":
            ET.SubElement(node_el, "icon", builtin="button_cancel")

        for child_id in node.children:
            build_node(node_el, nodes[child_id])

    build_node(root_el, nodes["0"])
    return ET.tostring(root_el, encoding="unicode")


def to_argdown(nodes: Dict[str, ClaimNode]) -> str:
    """Export argument map to Argdown syntax."""
    lines = [f"# {nodes['0'].text}", ""]

    def emit(nid: str, indent: int) -> None:
        node = nodes[nid]
        if nid != "0":
            prefix = "+" if node.relation == "SUPPORT" else "-"
            lines.append(("  " * indent) + f"{prefix} [{node.id}]: {node.text}")
        for cid in node.children:
            emit(cid, indent + (0 if nid == "0" else 1))

    emit("0", 0)
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse, audit, and export Argument Maps.")
    parser.add_argument("--input", required=True, help="Input shorthand text or file path.")
    parser.add_argument("--format", choices=["json", "mermaid", "freemind", "argdown", "audit"], default="audit")
    parser.add_argument("--output", help="Optional output file path.")
    args = parser.parse_args()

    in_path = Path(args.input)
    raw = in_path.read_text(encoding="utf-8") if in_path.is_file() else args.input

    nodes = parse_shorthand(raw)
    if args.format == "audit":
        out = json.dumps(audit_map(nodes), indent=2)
    elif args.format == "json":
        out = json.dumps({k: asdict(v) for k, v in nodes.items()}, indent=2)
    elif args.format == "mermaid":
        out = to_mermaid(nodes)
    elif args.format == "freemind":
        out = to_freemind_xml(nodes)
    elif args.format == "argdown":
        out = to_argdown(nodes)
    else:
        raise ValueError(f"Unsupported format: {args.format}")

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
