# Pesquisa para subir as notas baixas · 2026-09-18

Origem: auditoria de 24 h deu nota baixa a três itens (qualidade visual das fontes, loop de aprendizado, pré-requisitos de conta). Pesquisa feita por agente delegado nesta sessão, em fontes da Meta (via conector Meta Ads, texto integral dos artigos), repositórios no GitHub e relatos de fóruns. Marcação: **oficial** = Meta; **relato** = fórum, blog ou repositório de terceiros. Só entra o que decorre em ação para a bancada ou para a operação.

## 1. Erro de entrega `ad_not_approved_ctwa_number`

| Fonte | O que diz | Ação |
|---|---|---|
| oficial · facebook.com/business/help/4631406400243963 | Número da Plataforma WhatsApp (Cloud API) só serve para anúncio de clique após uma solicitação de conexão Página → número, aprovada por quem tem controle total do portfólio dono do número, na aba Solicitações das Configurações. | Abrir Configurações da Página > Contas vinculadas > WhatsApp e ver se a solicitação está pendente ou recusada; aprovar no Business Manager dono da WABA. |
| oficial · help/456220311516626 | Empresa não verificada deixa o número "pendente em análise"; verificação é pré-requisito para nome de exibição e limites. | Concluir a verificação da empresa (relato zenweb.my: decisão de 10 min a 14 dias úteis). |
| oficial · help/2091769220999799 e help/447934475640650 | "Número vinculado a outro business" exige remover o número como ativo do outro portfólio; o anúncio sempre usa o número conectado à Página escolhida. | Página, WABA e conta de anúncios no mesmo portfólio. |
| relato · msg91.com | Status "Pending" indefinido quando Página e número pertencem a Business Managers diferentes; some ao unificar a propriedade. | Idem. |
| relato · github facebook-nodejs-business-sdk issue 301 + referência oficial page_whatsapp_number_verification | Graph API: `GET /me/businesses?fields=owned_whatsapp_business_accounts{phone_numbers{display_phone_number,status,name_status,quality_rating}}`; vínculo via `POST /{page_id}/page_whatsapp_number_verification`; erros por anúncio em `issues_info` (no conector: `ads_get_errors`). | Rotina diária que grava status do número e erros dos anúncios no diário da campanha. Análise de anúncio leva cerca de 24 h (help/204798856225114); prazo do número não é publicado. |

## 2. Marcar compras nas conversas de WhatsApp

| Fonte | O que diz | Ação |
|---|---|---|
| oficial · help/1214599109289826 | "Maximizar compras via mensagens" exige ao menos 10 eventos de compra em 30 dias, pelo app WhatsApp Business ou Conversions API; a conversa precisa vir de anúncio de clique e ser marcada em até 7 dias do clique; rodar 7 dias e medir por compras na Meta. | Meta de operação: 10 compras marcadas em 30 dias. |
| oficial · mesma fonte | No app WhatsApp Business: Ferramentas > Atividade dos clientes > "Permitir que a Meta receba informações sobre eventos"; só as etiquetas predefinidas Novo pedido, Pagamento pendente, Pago, Pedido concluído atribuem; criar ou atualizar Pedido também conta. | Sem código: rotular todas as vendas a partir de hoje. |
| oficial · developers.facebook.com/docs/marketing-api/conversions-api/business-messaging | Robô próprio precisa de app Meta com acesso avançado a `whatsapp_business_management` e `whatsapp_business_manage_events`, dataset criado por WABA e `ctwa_clid` obrigatório, lido do webhook de mensagens da Cloud API. | Requisito para a Yara (Railway). |
| oficial · conversions-api/parameters/server-event | `action_source: business_messaging`; `event_time` no máximo 7 dias antes do envio, senão o lote inteiro é rejeitado. | Enviar a compra no dia da confirmação. |
| relato (código) · github TrackWhatsapp e prd_ctwa_clid | Payload em produção: `POST /{dataset_id}/events` com `event_name: Purchase`, `action_source: business_messaging`, `messaging_channel: whatsapp`, `user_data{whatsapp_business_account_id, ctwa_clid, ph[sha256]}`, `custom_data{currency: BRL, value}`; `ctwa_clid` vem em `referral` (`source_type: ad`, `source_id` = id do anúncio) da primeira mensagem. | A Yara salva `ctwa_clid` e `source_id` por contato na primeira mensagem; ao marcar "pago", dispara Purchase. `source_id` já dá atribuição por anúncio sem esperar a Meta. |

## 3. Andromeda, diversidade e leitura por criativo

| Fonte | O que diz | Ação |
|---|---|---|
| oficial · business/news "The creative advantage" (abr/2025) e engineering.fb.com (dez/2024) | Com Andromeda o foco sai da segmentação para a diversificação criativa: anúncios para pessoas e contextos diferentes, não versões da mesma ideia. | Mantém a regra da bancada: diferença material, não cosmética. |
| oficial · help/2720085414702598 | Anúncios demais ao mesmo tempo: cada um entrega menos e menos saem do aprendizado; combinar conjuntos e reduzir anúncios por conjunto mantendo criativos diversos. | 1 campanha, 1 conjunto amplo, lote pequeno e materialmente diferente. |
| oficial · help/269269737396981 e help/316478108955072 | Aprendizado limitado = improvável chegar a cerca de 50 eventos na semana após a última edição significativa; adicionar anúncio ao conjunto e trocar criativo são edições significativas. | Lançar lotes fechados, não anúncio a anúncio; ler 7 dias após a última edição. |
| oficial · help/203183363050448 | Com meta de custo por resultado, orçamento diário de ao menos 5 vezes o custo-alvo. | Regra derivada: 50 conversas em 7 dias vezes o custo por conversa atual = orçamento mínimo do conjunto. Não há mínimo oficial por criativo. |
| relato · segwise.ai e skaleit.agency (2026) | Teste citado: 1 conjunto com 25 criativos deu +17% conversões a −16% custo contra 5 conjuntos de 5; abaixo de US$ 100/dia, 1 campanha ampla com 6 ou mais criativos. | Leitura por `ad` nos Insights e `ads_get_creative_ads` para mapear creative_id → ad_id. |

## 4. Upscale em CPU mais rápido que Real-ESRGAN x2plus

| Fonte | O que diz | Ação |
|---|---|---|
| oficial (repo) · xinntao/Real-ESRGAN | `realesr-general-x4v3`: modelo pequeno para cenas gerais (1,21 M parâmetros, 4,65 MB) com `-dn` para controlar o denoise; CPU exige `--fp32`; issue 22 confirma CPU muito lenta nos modelos RRDB. | Trocar x2plus por general-x4v3 com `--outscale 2` e medir s/quadro. |
| oficial (repo) · Real-ESRGAN docs/anime_comparisons | Arquitetura compacta SRVGGNet: 65,9 fps em 640x480 numa V100; versão xs 9,5 vezes mais rápida que x4plus-anime. | Ordem de ganho esperada da arquitetura compacta. |
| oficial (repo) · opencv_contrib dnn_superres | CPU i7-9700K, 768x512 x4: FSRCNN 0,013 s, ESPCN 0,012 s, LapSRN 0,28 s, EDSR 3,27 s; PSNR FSRCNN 26,56 contra Lanczos 25,91. | FSRCNN via OpenCV como caminho de milissegundos quando o ganho do Real-ESRGAN não justificar 7 s/quadro. |
| oficial (repo) · k4yt3x/video2x e TNTwise/Universal-NCNN-Upscaler | AGPL-3.0; CPU exige AVX2; backends Real-ESRGAN ncnn, Anime4K, SPAN. | Só como ferramenta externa, nunca embutida. |
| oficial (repo) · pratik227/upscale_video_4k | MIT; Real-ESRGAN com fallback automático FSRCNN em CPU e remux de áudio via FFmpeg. | Reenquadrar e cortar antes do upscale para não ampliar pixels descartados. |

## 5. Reenquadramento 16:9 para 9:16 em CLI leve

| Fonte | O que diz | Ação |
|---|---|---|
| github fralapo/FrameShift | MIT; yolo11n + yolov11n-face (cerca de 11 MB), um crop fixo por cena; `python -m frameshift.main in.mp4 out.mp4 --ratio 9:16`; dependências sem versão fixada. | Candidato padrão para lote (produto parado). Fixar versões. |
| github KazKozDev/auto-vertical-reframe | MIT; YOLOv11-seg + ByteTrack + MediaPipe + PySceneDetect, câmera suavizada; Python 3.11, PyTorch 2.2+. | Quando há pessoa em movimento. |
| github mutonby/openshorts | MIT (core); MediaPipe + YOLOv8; CPU 5 a 8 min por vídeo de 8 min; pesado (Docker). | Só para clipes longos. |
| mediapipe AutoFlip | Apache-2.0; build Bazel com GPU desligada; parâmetro de estabilização decide câmera fixa ou tracking. | Referência. |

## Bloqueio de pesquisa registrado

developers.facebook.com, facebook.com, Reddit e a maioria dos blogs estão bloqueados pelo proxy desta sessão. Fontes oficiais vieram do conector Meta Ads (Central de Ajuda e docs em texto integral); relatos vieram de trechos de busca. Reddit não foi lido diretamente.

## O que muda na bancada (próximos passos técnicos)

1. `tools/upscale_realesrgan.py`: adicionar caminho `--model general-x4v3` (SRVGGNet) e fallback FSRCNN (OpenCV) para medir em CPU.
2. Nova estação de reenquadramento com FrameShift avaliado em 1 clipe de banco (edi-ofdr) antes de qualquer código.
3. `docs/ESTEIRA.md`, estação 10: registrar por `creative_id` os erros de entrega e o status do número a cada check-in diário.
4. Pré-requisitos de operação (não é código): aprovação do número na Página, verificação da empresa, etiquetas de pedido no WhatsApp Business, `ctwa_clid` capturado pela Yara.
