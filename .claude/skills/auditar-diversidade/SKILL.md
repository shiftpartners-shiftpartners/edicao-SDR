---
name: auditar-diversidade
description: Verifica se as variantes de um lote são materialmente diferentes (Andromeda) e não gêmeas cosméticas, com cobertura por conceito/hook/execução/formato. Use antes de fechar um lote ou quando pedirem "são variantes de verdade?".
---

# Auditar diversidade

```bash
python scripts/diversity_check.py media/work/ledger.jsonl --out media/work/diversidade-v01.md
```

- `FAIL`: duas variantes com a mesma assinatura (conceito, hook, execução, formato, duração) declaradas como diferença material. Corrija a assinatura ou marque `material_difference: false`.
- `WARN`: linha com um só conceito. Aceitável só com justificativa registrada.
- Cobertura vazia não é problema de script; é decisão de produção.

O script não prevê performance e não fala com a Meta. Ele só mantém o registro honesto. Diferença material está definida em `docs/ANDROMEDA.md`.
