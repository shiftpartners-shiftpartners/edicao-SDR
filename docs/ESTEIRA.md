# Esteira de produção · O Segredo da Roça e Família da Roça

Uma linha só, com o olhar da Andromeda: a Meta recupera anúncios por diferença material e devolve sinal por `creative_id`. A esteira existe para produzir, medir e aprender em ciclo, não para gerar volume. Cada estação tem um script, um responsável e um gate. Nada passa de estação sem o gate.

## Estações

| # | Estação | Comando | Gate para seguir | Saída |
|---|---|---|---|---|
| 0 | Entrada de material | Drive (até 10 MB) ou anexo na conversa; `make normalize SRC=...` para clipes de celular que o FFmpeg recusa | decodifica pelo filtro | `media/source/` (original intacto; `.rangefix` quando preciso) |
| 1 | Inventário | `make inventory`, `make sheet SRC=...` | contact sheet lido por humano ou agente; cena classificada | `footage-index-*.json`, `media/contact-sheets/` |
| 2 | Brief e verdade | `brief.<lote>.yaml` com fonte de cada fato | guardião da verdade libera preço, brinde, prazo, rota | brief |
| 3 | Conceitos | matriz conceito × hook × execução × formato | cada linha muda tese, hook ou execução; cosmético não conta | `matriz-variantes.md` |
| 4 | Plano de corte | `<id>.edit-plan.yaml` por peça | timeline com fonte, in/out, texto em tela; sem claim fora do brief | EDP |
| 5 | Esteira | `make lote LOTE=media/work/<lote>` | dry-run, render, rascunho com legenda e locução, QC técnico, ledger e diversidade em um comando | renders, `-draft.mp4`, `.qc.json`, `RELATORIO_ESTEIRA-*.md` |
| 6 | Upscale (só quando a fonte é menor que 720p) | `tools/upscale_realesrgan.py <fonte> --start --duration` | só a faixa usada pelo EDP; EDP aponta para o `.esrgan2x` | fonte irmã em 2x |
| 7 | Decisão | `DECISAO_ARQUITETO.md` + ledger (`status`, `human_approval`) | QC pass, verdade liberada, diferença material; risco aceito escrito | ledger aprovado |
| 8 | Handoff | `make handoff ID=... OBJ=... BY=...` | só `approved`; pacote com hipótese e sinal a observar | `handoff-*.md` |
| 9 | Acabamento final | CapCut: trilha baixa, fonte da marca, logo, a partir do `.ass` e do rascunho | QC final no MP4 exportado | MP4 para mídia |
| 10 | Veiculação e observação | operação de mídia, com aprovação humana; observação em 7 dias por `creative_id` | pré-requisitos: número de WhatsApp aprovado, compra marcada na conversa | `performance-observations.jsonl` → decisão escalar, iterar, pausar |

A esteira (estação 5) nunca aprova nem publica. Ela para em `qc_pending` e escreve o relatório para a decisão humana ou do Arquiteto por delegação registrada.

## O que foi colhido de fora e onde encaixa

Regra: nunca o repositório inteiro; só a peça que resolve uma estação, com licença conferida e teste próprio.

| Estação | Componente externo | O que exatamente entrou |
|---|---|---|
| 0, 5 | FFmpeg (libx264, aac, libass, loudnorm, amix, h264_metadata) | chamadas CLI restritas nos scripts; nenhum código copiado |
| 6 | Real-ESRGAN (xinntao) | arquitetura RRDBNet reescrita em torch puro em `tools/upscale_realesrgan.py`; pesos x2plus baixados à parte |
| 4b | faster-whisper | adapter opcional para transcrição; não obrigatório |
| 5 | padrão director / refiner / reviewer (agentic-video-editor, forwrdcut) | separação de papéis nos agentes `.claude/agents/`; sem código importado |
| 1 | PySceneDetect | opcional, não instalado; contact sheet próprio cobre o inventário |
| 10 | Meta Andromeda (publicação de engenharia) | critério de diferença material e rastreio por `creative_id` no ledger e na auditoria |

## Cadência

Lote diário: entrada de material de manhã, esteira ao meio-dia, decisão e handoff à tarde, acabamento e veiculação até o fim do dia. Observação a cada 7 dias alimenta a próxima matriz. Uma peça por conceito por rodada; hooks alternativos só onde o conceito venceu.
