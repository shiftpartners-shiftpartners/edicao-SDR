---
name: handoff-midia
description: Gera o pacote de handoff para a operação de mídia com creative_id, hipótese, QC e aprovação humana, conforme docs/MEASUREMENT_CONTRACT.md. Use quando uma peça for aprovada e precisar sair da bancada.
---

# Handoff para mídia

Pré-requisito: ledger com `human_approval: approved` para o `creative_id` e QC técnico `pass`.

```bash
python scripts/handoff_pack.py media/work/ledger.jsonl <creative_id> \
  --objective "<objetivo informado pela operação>" \
  --approved-by "<nome/papel>" --approved-on 2026-09-18 \
  --qc-report media/renders/<id>__v01.qc.json \
  --out media/work/handoff-<creative_id>.md
```

- Sem aprovação humana o script recusa; `--draft` gera prévia marcada como não aprovada.
- O handoff não define público, orçamento ou placement. Isso é da operação de mídia.
- Quando voltarem dados, registre observação em JSONL (`templates/performance-observations.example.jsonl`) e valide com `scripts/validate_records.py`. Decisão: `escalar | iterar | pausar | inconclusivo`, sempre humana (`docs/LEARNING_LOOP.md`).
