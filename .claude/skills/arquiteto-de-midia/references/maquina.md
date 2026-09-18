# Máquina de edição SDR — etapa × comando × agente

Repositório: `shiftpartners-shiftpartners/edicao-SDR`. Mídia bruta fica em `media/source/` fora do Git.

| Etapa | Comando | Agente | Saída |
|---|---|---|---|
| 1. Inventário | `python scripts/media_probe.py media/source --out media/work/footage-index-v01.json --hash` · `python scripts/contact_sheet.py <video> --out media/contact-sheets/<nome>.png --frames 16` | `preprocessador` | índice JSON, pranchas PNG |
| 2–4. Direção | brief + matriz + EDP a partir de `templates/` · `python scripts/validate_records.py media/work/ledger.jsonl --schema schemas/creative-variant.schema.json` | `diretor-criativo` + `guardiao-da-verdade` | brief, matriz, EDP YAML, ledger JSONL |
| 5. Refino e conversão | `python scripts/edp_to_render_plan.py <edp.yaml> --out <plan.json> --unsupported report` | `refinador-de-corte` | render-plan JSON v1 + lista de acabamento |
| 5b. Legenda | `python scripts/caption_segments.py <transcript.json> --out <legenda.json> --srt <legenda.srt>` | `refinador-de-corte` | blocos de 3–5 palavras + SRT |
| 6. Render | `python scripts/render_plan.py <plan.json> --source-root media/source --out media/renders/<id>__v01.mp4` (dry-run) e depois `--execute` | `renderer` | MP4 1080p H.264/AAC + relatório `.mp4.json` |
| 7. QC | `python scripts/qc_render.py <mp4> --template meta-ad --out <id>.qc.json` (templates em `templates/osdr-formats.json`) + prancha do render | `revisor-qc` + `guardiao-da-verdade` | `.qc.json`, parecer |
| 8. Diversidade | `python scripts/diversity_check.py media/work/ledger.jsonl` | `revisor-qc` | relatório Markdown |
| 9. Handoff | `python scripts/handoff_pack.py media/work/ledger.jsonl <creative_id> --objective "..." --approved-by "..." --qc-report <id>.qc.json` | humano aprova | handoff Markdown |

Atalhos: `make check`, `make inventory`, `make plan ID=x`, `make dry-run ID=x`, `make render ID=x`, `make qc ID=x`, `make handoff ID=x OBJ=... BY=...`.

Convenção de nome: `<produto>__c<conceito>__h<hook>__e<execucao>__<formato>__v<versao>.mp4`.

## O que o renderer v1 faz e não faz

Faz: cortes sequenciais, pad sem cortar produto, 9:16 / 4:5 / 1:1 / 16:9, 30 fps, H.264/AAC, hash e três checagens.
Não faz: legenda queimada, trilha, transição, reframe automático, imagem estática, multicamada. Isso é acabamento humano.

## Regra de retry

Crop ruim → refinador/editor · hook fraco → diretor · claim não aprovado → diretor/brief · silêncio sobrando → refinador · codec ou áudio quebrado → renderer.
