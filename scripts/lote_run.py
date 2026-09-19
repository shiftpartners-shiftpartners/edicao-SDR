#!/usr/bin/env python3
"""Esteira de produção: runs one lote end to end with the existing stage scripts.

One manifest (`lote.yaml`) drives everything; every stage keeps its own guarantees
(dry-run before render, never overwrite, QC before approval, diversity before handoff).
The esteira never approves: it stops at `qc_pending` and writes a report for the
Arquiteto de Mídia decision. Existing outputs are skipped and reported, so re-running
a lote after adding pieces only produces what is missing.

Manifest (media/work/<lote>/lote.yaml):
  id: kitcozinha-t1t6
  product_line: kit-cozinha
  template: reel15            # QC template (SDR) or format/duration for FDR
  format: "9:16"              # used when the bench has no templates
  max_seconds: 16             # idem
  renders_dir: media/renders/<lote>
  pieces:
    - id: t2                  # edit plan: <lote>/kitcozinha-t2.edit-plan.yaml
      edp: kitcozinha-t2.edit-plan.yaml
      output: kitcozinha__t2__9x16__v01      # render name without extension
      vo: vo/T2_comida_take1.mp3             # optional
      vo_delay_ms: 300                       # optional
"""
import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run(cmd, log):
    result = subprocess.run(cmd, capture_output=True, text=True)
    log.append({"cmd": " ".join(str(c) for c in cmd), "returncode": result.returncode,
                "stdout_tail": result.stdout[-400:], "stderr_tail": result.stderr[-400:]})
    return result


def sources_of(edp_path):
    edp = yaml.safe_load(edp_path.read_text(encoding="utf-8"))
    return sorted({clip["source"] for clip in edp["timeline"]})


def qc_verdict(path):
    if not path.exists():
        return "sem QC"
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("technical_verdict", "?")
    except json.JSONDecodeError:
        return "QC ilegível"


def process_piece(piece, lote_dir, renders_dir, source_root, manifest, log, dry_run):
    py = sys.executable
    edp = lote_dir / piece["edp"]
    plan = lote_dir / (Path(piece["edp"]).name.replace(".edit-plan.yaml", ".render-plan.json"))
    render = renders_dir / f"{piece['output']}.mp4"
    draft = renders_dir / f"{piece['output']}-draft.mp4"
    row = {"piece": piece["id"], "edp": edp.name, "render": "", "draft": "", "qc": "", "notes": []}
    if not edp.exists():
        row["notes"].append("EDP não encontrado")
        return row
    # 0. sources must decode through filters (invalid colour range guard)
    missing = [s for s in sources_of(edp) if not (source_root / s).exists()]
    if missing:
        row["notes"].append("fonte ausente: " + ", ".join(missing))
        return row
    check = run([py, SCRIPTS / "normalize_source.py", "--check", *[source_root / s for s in sources_of(edp)]], log)
    if check.returncode != 0:
        row["notes"].append("fonte não decodifica; rode make normalize SRC=... e aponte o EDP para o .rangefix")
        return row
    # 1. plan (report unsupported items instead of failing; that list is the human finishing)
    if plan.exists():
        row["notes"].append("render-plan já existia (mantido)")
    else:
        conv = run([py, SCRIPTS / "edp_to_render_plan.py", edp, "--out", plan, "--unsupported", "report"], log)
        if conv.returncode != 0:
            row["notes"].append("conversão falhou: " + conv.stderr.strip()[-200:])
            return row
    # 2. dry-run then render
    if render.exists():
        row["render"] = "existia"
    else:
        dry = run([py, SCRIPTS / "render_plan.py", plan, "--source-root", source_root, "--out", render], log)
        if dry.returncode != 0 or "failed" in dry.stdout:
            row["notes"].append("dry-run falhou")
            return row
        if dry_run:
            row["render"] = "dry-run ok"
            return row
        rend = run([py, SCRIPTS / "render_plan.py", plan, "--source-root", source_root, "--out", render, "--execute"], log)
        row["render"] = "ok" if render.exists() else "falhou"
        if not render.exists():
            row["notes"].append(rend.stdout.strip()[-200:] or rend.stderr.strip()[-200:])
            return row
    # 3. draft finishing (captions from EDP + optional VO + loudnorm)
    if draft.exists():
        row["draft"] = "existia"
    else:
        cmd = [py, SCRIPTS / "finish_draft.py", edp, render, "--out", draft]
        if piece.get("vo"):
            cmd += ["--vo", lote_dir / piece["vo"], "--vo-delay-ms", str(piece.get("vo_delay_ms", 300))]
        fin = run(cmd, log)
        row["draft"] = "ok" if draft.exists() else "falhou: " + fin.stderr.strip()[-120:]
    # 4. technical QC on the draft (what a human will watch)
    target = draft if draft.exists() else render
    qc_path = target.with_suffix(".qc.json")
    if not qc_path.exists():
        cmd = [py, SCRIPTS / "qc_render.py", target, "--out", qc_path]
        if manifest.get("template"):
            cmd += ["--template", manifest["template"]]
        else:
            cmd += ["--format", manifest.get("format", "9:16")]
            if manifest.get("max_seconds"):
                cmd += ["--max-seconds", str(manifest["max_seconds"])]
            if manifest.get("min_seconds"):
                cmd += ["--min-seconds", str(manifest["min_seconds"])]
        run(cmd, log)
    row["qc"] = qc_verdict(qc_path)
    return row


def main():
    parser = argparse.ArgumentParser(description="Run a whole lote through the bench (esteira). Never approves.")
    parser.add_argument("lote_dir", type=Path, help="directory with lote.yaml and the edit plans")
    parser.add_argument("--source-root", type=Path, default=ROOT / "media" / "source")
    parser.add_argument("--dry-run", action="store_true", help="stop after the dry-run of each piece")
    parser.add_argument("--report", type=Path, help="Markdown report path (default: <lote>/RELATORIO_ESTEIRA-<timestamp>.md)")
    args = parser.parse_args()
    manifest = yaml.safe_load((args.lote_dir / "lote.yaml").read_text(encoding="utf-8"))
    renders_dir = Path(manifest.get("renders_dir", f"media/renders/{args.lote_dir.name}"))
    if not renders_dir.is_absolute():
        renders_dir = ROOT / renders_dir
    renders_dir.mkdir(parents=True, exist_ok=True)
    log, rows = [], []
    for piece in manifest.get("pieces", []):
        rows.append(process_piece(piece, args.lote_dir, renders_dir, args.source_root, manifest, log, args.dry_run))
    # 5. ledger + diversity (Andromeda gate) when a ledger exists
    ledger = args.lote_dir / "ledger.jsonl"
    diversity = "sem ledger ainda (criar antes da decisão do Arquiteto)"
    if ledger.exists():
        val = run([sys.executable, SCRIPTS / "validate_records.py", "--schema", ROOT / "schemas" / "creative-variant.schema.json", ledger], log)
        div = run([sys.executable, SCRIPTS / "diversity_check.py", ledger, "--report-only"], log)
        diversity = ("ledger válido; " if val.returncode == 0 else "LEDGER INVÁLIDO; ") + \
                    ("sem colisão cosmética" if div.returncode == 0 and "Nenhuma colisão" in div.stdout else "COLISÃO ou erro na auditoria")
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report = args.report or args.lote_dir / f"RELATORIO_ESTEIRA-{stamp}.md"
    if report.exists():
        sys.exit(f"recusado: {report} já existe")
    lines = [f"# Relatório da esteira · {manifest.get('id', args.lote_dir.name)} · {stamp}", "",
             f"Linha: {manifest.get('product_line', '?')} · QC: {manifest.get('template') or manifest.get('format', '9:16')} · "
             f"renders em `{renders_dir.relative_to(ROOT) if renders_dir.is_relative_to(ROOT) else renders_dir}`", "",
             "| Peça | EDP | Render | Rascunho (legenda+VO) | QC técnico | Observações |", "|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['piece']} | {r['edp']} | {r['render']} | {r['draft']} | {r['qc']} | {'; '.join(r['notes'])} |")
    lines += ["", f"Diversidade (gate Andromeda): {diversity}", "",
              "Próximo passo humano: revisar os rascunhos no celular, registrar a decisão do Arquiteto no ledger "
              "(`status`, `human_approval`) e só então gerar handoff. A esteira não aprova.", ""]
    report.write_text("\n".join(lines), encoding="utf-8")
    (report.with_suffix(".log.json")).write_text(json.dumps(log, indent=1, ensure_ascii=False), encoding="utf-8")
    print("\n".join(lines))
    failed = [r for r in rows if r["qc"] not in ("pass",) and not args.dry_run]
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
