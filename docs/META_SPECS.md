# Especificações Meta para vídeo — referência de bancada

Classificação: **referência técnica provisória**. Valores abaixo refletem a orientação pública da Meta conhecida em 2026-09; a Central de Ajuda muda sem aviso. Antes de subir um lote, conferir a página oficial de especificações do placement e registrar a data da conferência aqui.

## Formatos que a bancada renderiza

| Formato | Pixels (render v1) | Placements típicos |
|---|---|---|
| 9:16 | 1080×1920 | Reels, Stories, feed vertical |
| 4:5 | 1080×1350 | Feed Instagram/Facebook |
| 1:1 | 1080×1080 | Feed, catálogo |
| 16:9 | 1920×1080 | in-stream, site |

Container MP4, H.264, AAC 48 kHz estéreo, 30 fps, `yuv420p`, `faststart`. É o que `scripts/render_plan.py` entrega e `scripts/qc_render.py` confere.

## Área segura em 9:16 (orientação pública)

Manter texto, legenda, logo e CTA fora de aproximadamente **14% do topo (~250 px)** e **20% da base (~340 px)** em 1080×1920, onde a interface do Reels/Stories sobrepõe elementos. Conferir sempre no celular; o contact sheet do render ajuda a ver a posição da legenda.

## Duração

Reels e Stories aceitam vídeos curtos; anúncios de conversão do OSDR trabalham entre 6 e 9 s (`templates/osdr-formats.json`). A Meta permite durações bem maiores; o limite curto é decisão editorial, não técnica.

## Andromeda e diversidade

A Meta descreve Andromeda como sistema de ads retrieval para um universo muito maior de criativos (`docs/ANDROMEDA.md`). Consequência para esta bancada: entregar variantes materialmente diferentes, rastreáveis por `creative_id`, e nunca atribuir à Meta regras que ela não publicou (quantidade de conceitos, formatos obrigatórios, "o algoritmo prefere X").

## Transparência e IA

Alteração significativa de imagem ou uso de IA generativa deve estar registrado no ledger (`notes`) para conferência das regras de transparência aplicáveis no momento da veiculação.

## Registro de conferência

| Data | Quem | Página conferida | Mudou algo? |
|---|---|---|---|
| — | — | — | — |
