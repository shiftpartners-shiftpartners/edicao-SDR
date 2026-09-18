---
name: renderizar-corte
description: Converte EDP aprovado em render-plan JSON v1, valida em dry-run e renderiza cortes sequenciais com FFmpeg sem destruir a fonte. Use quando pedirem "renderiza", "gera o corte", "exporta a versão".
---

# Renderizar corte

1. Refine timestamps e converta (agente `refinador-de-corte`):
   ```bash
   python scripts/edp_to_render_plan.py media/work/<id>.edit-plan.refined.yaml --out media/work/<id>.render-plan.json
   ```
   Com `crop`/`text_overlay` no EDP, use `--unsupported report` e leve o acabamento para editor humano.
2. Dry-run obrigatório:
   ```bash
   python scripts/render_plan.py media/work/<id>.render-plan.json --source-root media/source --out media/renders/<id>__v01.mp4
   ```
3. Render (agente `renderer`):
   ```bash
   python scripts/render_plan.py media/work/<id>.render-plan.json --source-root media/source --out media/renders/<id>__v01.mp4 --execute
   ```
4. Nunca sobrescreva; incremente `v`. O relatório `.mp4.json` fica ao lado do render.

Limites do renderer v1 estão em `docs/SETUP.md`: sem legenda queimada, trilha, transição, reframe automático ou multicamada. Não contorne por shell manual.
