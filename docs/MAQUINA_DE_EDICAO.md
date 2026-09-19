# Máquina de edição — mapa operacional (O Segredo da Roça)

Este documento liga cada etapa do pipeline ao script que executa, ao agente que opera e à skill que o operador chama. Nada aqui publica, altera campanha ou toca em `media/source/`.

## Etapas × scripts × agentes × skills

| Etapa | Script executável | Agente (`.claude/agents/`) | Skill (`.claude/skills/`) | Saída versionada |
|---|---|---|---|---|
| 1. Inventário | `scripts/media_probe.py`, `scripts/contact_sheet.py` | `preprocessador` | `inventariar-material` | `media/work/footage-index-vNN.json`, `media/contact-sheets/*.png` |
| 2. Direção criativa | `scripts/validate_records.py`, `scripts/diversity_check.py` | `diretor-criativo` + `guardiao-da-verdade` | `planejar-edicao`, `arquiteto-de-midia` | brief, matriz, EDP YAML, ledger JSONL |
| 3. Refino de corte | `scripts/edp_to_render_plan.py` | `refinador-de-corte` | `renderizar-corte` | `*.edit-plan.refined.yaml`, `*.render-plan.json` |
| 4. Render | `scripts/render_plan.py` | `renderer` | `renderizar-corte` | `media/renders/<id>__vNN.mp4` + `.mp4.json` |
| 4b. Legenda | `scripts/caption_segments.py` | `refinador-de-corte` | `renderizar-corte` | `legenda-vNN.json`, `legenda-vNN.srt` (acabamento humano) |
| 4c. Rascunho de acabamento | `scripts/finish_draft.py` (legendas do EDP + locução + loudnorm) | `renderer` | `renderizar-corte` | `*-draft.mp4` + `.ass` para revisão no celular; acabamento final continua humano |
| 5b. Esteira (todas as estações em um comando) | `scripts/lote_run.py` (`make lote LOTE=...`) | orquestra `preprocessador` → `renderer` → `revisor-qc`; não aprova | todas | `RELATORIO_ESTEIRA-*.md` + log; ver `docs/ESTEIRA.md` |
| 0b. Saneamento de fonte | `scripts/normalize_source.py` | `preprocessador` | `inventariar-material` | `*.rangefix.mp4` (irmão remuxado; original intacto) |
| 5. QC | `scripts/qc_render.py --template`, `scripts/contact_sheet.py` | `revisor-qc` + `guardiao-da-verdade` | `qc-render` | `*.qc.json`, parecer curto |
| 6. Diversidade do lote | `scripts/diversity_check.py` | `revisor-qc` | `auditar-diversidade` | `diversidade-vNN.md` |
| 7. Aprovação humana | `scripts/validate_records.py` | ninguém: humano | — | ledger com `human_approval: approved` |
| 8. Handoff | `scripts/handoff_pack.py` | — | `handoff-midia` | `handoff-<creative_id>.md` |
| 9. Observação e decisão | `scripts/validate_records.py` | — | `handoff-midia` | `performance-observations.jsonl` |
| 10. Auditoria de campanha viva | `docs/CHECKLIST_AUDITORIA_META.md` (30 itens, só leitura da API) | `auditor-de-trafego-meta` | `auditar-campanha-meta` | `AUDITORIA_CAMPANHA_<id>_<data>_<hora>.md` versionado, sem editar nada na Meta |

Padrão editorial da casa: `docs/PADRAO_EDICAO_OSDR.md`. Templates por formato: `templates/osdr-formats.json`. Specs Meta: `docs/META_SPECS.md`.

## Contratos entre etapas

- **Brief → Diretor:** só `fontes_confirmadas` viram claim. Lacuna vira `pendencias_humanas`.
- **EDP (YAML) → Render (JSON v1):** o conversor carrega apenas cortes sequenciais. `crop`, `text_overlay`, transição, trilha e velocidade vão para acabamento humano e ficam listados, nunca ignorados em silêncio.
- **Render → QC:** o render entrega hash, duração e três checagens; o QC técnico acrescenta codec, geometria, fps, abertura preta, mudez e clipping. Criativo e verdade continuam humanos/agentes.
- **Ledger → Handoff:** `creative_id` é a chave de junção. Handoff sem `human_approval: approved` só sai como rascunho.
- **Observação → Decisão:** `null` não é zero; decisão sempre `decided_by_human: true`.

## Regra de retry

Falha volta ao estágio responsável (`docs/PIPELINE.md`). O Renderer não corrige hook; o Diretor não corrige codec.

## Comandos de conferência

```bash
make check          # testes + validação de exemplos + auditoria de diversidade
make inventory      # índice técnico versionado por timestamp
make plan ID=x      # EDP YAML → render-plan JSON
make dry-run ID=x   # valida sem renderizar
make render ID=x    # renderiza (não sobrescreve)
make qc ID=x TEMPLATE=meta-ad
make handoff ID=x OBJ="conversas qualificadas" BY="nome/papel"
```

## O que a máquina não faz

Não publica, não sobe criativo para a Meta, não escolhe público, orçamento ou placement, não infere regra de Andromeda, não aprova peça. Esses pontos são humanos por decisão, não por limitação temporária.
