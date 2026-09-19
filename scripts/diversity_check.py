#!/usr/bin/env python3
"""Audit a creative ledger for material creative diversity.

Andromeda-oriented production needs variants that differ materially, not
cosmetically. This script does not talk to Meta and does not predict
performance; it only reports what the ledger claims and where claims collide.
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

DIMENSIONS = ("concept", "hook", "execution", "format", "duration_seconds")


def signature(record):
    return (
        record.get("concept", {}).get("id"),
        record.get("hook", {}).get("id"),
        record.get("execution", {}).get("id"),
        record.get("format"),
        record.get("duration_seconds"),
    )


def load(path):
    rows = []
    for line, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if raw.strip():
            record = json.loads(raw)
            if not isinstance(record, dict) or "creative_id" not in record:
                raise ValueError(f"line {line}: record without creative_id")
            rows.append(record)
    if not rows:
        raise ValueError("empty ledger")
    return rows


def audit(records):
    findings = []
    by_line = defaultdict(list)
    for record in records:
        by_line[record.get("product_line") or "(sem linha)"].append(record)
    coverage = {}
    for line, rows in sorted(by_line.items()):
        active = [r for r in rows if r.get("status") != "archived"]
        concepts = {r.get("concept", {}).get("id") for r in active}
        hooks = {r.get("hook", {}).get("id") for r in active}
        executions = {r.get("execution", {}).get("id") for r in active}
        formats = {r.get("format") for r in active}
        coverage[line] = {"variants": len(active), "concepts": len(concepts), "hooks": len(hooks),
                          "executions": len(executions), "formats": len(formats)}
        if len(active) >= 2 and len(concepts) == 1:
            findings.append({"severity": "warn", "product_line": line,
                             "message": "todas as variantes ativas executam o mesmo conceito; diversidade só de hook/execução"})
        seen = defaultdict(list)
        for record in active:
            seen[signature(record)].append(record)
        for sig, group in seen.items():
            ids = sorted({g["creative_id"] for g in group})
            if len(ids) > 1 and any(g.get("material_difference") for g in group):
                findings.append({"severity": "fail", "product_line": line, "creative_ids": ids,
                                 "message": "mesma assinatura conceito/hook/execução/formato/duração declarada como diferença material"})
        for record in active:
            parent = record.get("parent_creative_id")
            if parent:
                parent_record = next((r for r in records if r["creative_id"] == parent), None)
                if parent_record and signature(parent_record) == signature(record) and record.get("material_difference"):
                    findings.append({"severity": "fail", "product_line": line, "creative_ids": [parent, record["creative_id"]],
                                     "message": "variante filha idêntica ao pai em todas as dimensões, mas marcada como diferença material"})
    return coverage, findings


def render_markdown(coverage, findings):
    lines = ["# Auditoria de diversidade criativa", "",
             "| Linha | Variantes ativas | Conceitos | Hooks | Execuções | Formatos |", "|---|---:|---:|---:|---:|---:|"]
    for line, c in coverage.items():
        lines.append(f"| {line} | {c['variants']} | {c['concepts']} | {c['hooks']} | {c['executions']} | {c['formats']} |")
    lines += ["", "## Achados", ""]
    if not findings:
        lines.append("Nenhuma colisão encontrada. Isso não prova diferença material; prova apenas que o registro é consistente.")
    for f in findings:
        ids = ", ".join(f.get("creative_ids", [])) or "-"
        lines.append(f"- **{f['severity'].upper()}** · {f['product_line']} · {f['message']} ({ids})")
    lines += ["", "Regra: diferença material exige mudança de tese, hook, ordem narrativa, demonstração, protagonista, ritmo, linguagem visual, duração, CTA ou enquadramento. Cor, legenda ou transição sozinhas não contam.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Audit material diversity in a creative ledger (JSONL).")
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--out", type=Path, help="write Markdown report (must not exist)")
    parser.add_argument("--report-only", action="store_true", help="exit 0 even with failures")
    args = parser.parse_args()
    try:
        coverage, findings = audit(load(args.ledger))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(2, f"audit failed: {exc}\n")
    text = render_markdown(coverage, findings)
    if args.out:
        if args.out.exists() or args.out.is_symlink():
            parser.exit(1, "report already exists; choose a new version\n")
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    print(text)
    failed = any(f["severity"] == "fail" for f in findings)
    sys.exit(1 if failed and not args.report_only else 0)


if __name__ == "__main__":
    main()
