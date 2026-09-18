#!/usr/bin/env python3
"""Build the media handoff document for one creative_id from the ledger.

Implements docs/MEASUREMENT_CONTRACT.md: the handoff carries identity,
hypothesis and approval so that later observations can be joined back.
"""
import argparse
import json
from datetime import date
from pathlib import Path


def load_record(ledger, creative_id):
    for raw in ledger.read_text(encoding="utf-8").splitlines():
        if raw.strip():
            record = json.loads(raw)
            if record.get("creative_id") == creative_id:
                return record
    raise ValueError(f"creative_id not found in ledger: {creative_id}")


def build(record, objective, approved_by, approved_on, qc_report=None, draft=False):
    approved = record.get("human_approval") == "approved"
    if not approved and not draft:
        raise ValueError("creative is not human-approved; use --draft to produce a non-approved preview")
    title = "RASCUNHO · NÃO APROVADO" if (draft and not approved) else "HANDOFF PARA MÍDIA"
    lines = [f"# {title} · {record['creative_id']}", "",
             "| Campo | Valor |", "|---|---|",
             f"| creative_id | `{record['creative_id']}` |",
             f"| asset_filename | `{record.get('asset_filename')}` |",
             f"| produto/linha | {record.get('product_line') or 'null'} |",
             f"| conceito | {record.get('concept', {}).get('id')} · {record.get('concept', {}).get('summary')} |",
             f"| hook | {record.get('hook', {}).get('id')} · {record.get('hook', {}).get('summary')} |",
             f"| execução | {record.get('execution', {}).get('id')} · {record.get('execution', {}).get('summary')} |",
             f"| formato / duração | {record.get('format')} / {record.get('duration_seconds')}s |",
             f"| versão | v{record.get('version')} |",
             f"| hipótese | {record.get('hypothesis')} |",
             f"| variável principal | {record.get('primary_variable')} |",
             f"| variante-mãe | {record.get('parent_creative_id') or 'null'} |",
             f"| objetivo de mídia | {objective} |",
             f"| aprovado por | {approved_by if approved else 'PENDENTE'} |",
             f"| data da aprovação | {approved_on if approved else 'PENDENTE'} |",
             f"| status no ledger | {record.get('status')} / human_approval={record.get('human_approval')} |"]
    if qc_report:
        lines += ["", "## QC técnico automático", "",
                  f"- veredito: **{qc_report.get('technical_verdict')}** · sha256 `{qc_report.get('sha256')}` · {qc_report.get('duration_seconds')}s"]
        for c in qc_report.get("checks", []):
            lines.append(f"- {c['status']}: {c['name']} ({c['detail']})")
    lines += ["", "## Regras do contrato", "",
              "- `creative_id` é a chave de junção com a observação de performance.",
              "- Objetivo, público, orçamento e placement são decididos pela operação de mídia, não por este repositório.",
              "- Observações voltam com janela, timezone, moeda, denominadores e mudanças concorrentes (`schemas/performance-observation.schema.json`).",
              "- Ausência de dado é `null`, nunca zero.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate a Markdown handoff for one creative_id.")
    parser.add_argument("ledger", type=Path)
    parser.add_argument("creative_id")
    parser.add_argument("--objective", required=True, help="media objective stated by the responsible person")
    parser.add_argument("--approved-by", default="", help="name/role of the human approver")
    parser.add_argument("--approved-on", default=date.today().isoformat())
    parser.add_argument("--qc-report", type=Path, help="JSON from scripts/qc_render.py")
    parser.add_argument("--draft", action="store_true")
    parser.add_argument("--out", type=Path, help="write Markdown (must not exist)")
    args = parser.parse_args()
    try:
        record = load_record(args.ledger, args.creative_id)
        if record.get("human_approval") == "approved" and not args.approved_by:
            parser.exit(1, "approved creative requires --approved-by\n")
        qc = json.loads(args.qc_report.read_text(encoding="utf-8")) if args.qc_report else None
        text = build(record, args.objective, args.approved_by, args.approved_on, qc, args.draft)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(1, f"handoff failed: {exc}\n")
    if args.out:
        if args.out.exists() or args.out.is_symlink():
            parser.exit(1, "output already exists; choose a new version\n")
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
