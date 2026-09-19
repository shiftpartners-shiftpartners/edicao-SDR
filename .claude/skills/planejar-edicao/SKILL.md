---
name: planejar-edicao
description: Fecha conceito, matriz conceito×hook×execução×formato e Edit Decision Plan (YAML) a partir de brief aprovado e inventário. Use quando pedirem cortes, variações, hooks, plano de edição ou "monte X versões".
---

# Planejar edição

Pré-requisitos: brief preenchido a partir de `templates/brief.example.yaml` com `fontes_confirmadas`; inventário concluído (`inventariar-material`).

1. Leia `.claude/skills/arquiteto-de-midia/SKILL.md`, `docs/PADRAO_EDICAO_OSDR.md`, `templates/osdr-formats.json` e `docs/ANDROMEDA.md`. Escolha o template pelo objetivo.
2. Defina conceitos materialmente diferentes (tese, hook, narrativa, demonstração, protagonista, ritmo, CTA, formato). Cor/legenda/transição não contam.
3. Preencha a matriz a partir de `templates/variant-matrix.example.md`; marque diferença material com justificativa.
4. Escreva um EDP por variante a partir de `templates/edit-plan.example.yaml`. `source` é nome de arquivo em `media/source/`; `in`/`out` em `HH:MM:SS.mmm`.
5. Cadastre cada variante no ledger (`templates/creative-ledger.example.jsonl` como modelo) com `hypothesis` e `primary_variable`, status `draft`, e valide:
   ```bash
   python scripts/validate_records.py media/work/ledger.jsonl --schema schemas/creative-variant.schema.json
   python scripts/diversity_check.py media/work/ledger.jsonl
   ```
6. Passe pelo agente `guardiao-da-verdade` antes de enviar o EDP para aprovação.

Delegue a criação ao agente `diretor-criativo`. Saída sempre com `human_approval: required`.
