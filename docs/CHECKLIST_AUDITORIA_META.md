# Checklist de auditoria de campanha Meta (conversas no WhatsApp)

Cada bloco lista o campo de API a ler, o critério de OK e a evidência mínima. Veredito por item: OK, FALHA, RISCO, NÃO LIDO. Sem valor bruto lido, o item é NÃO LIDO.

| # | Bloco | Item | Campo/ferramenta | Critério de OK | Evidência mínima |
|---|---|---|---|---|---|
| 1 | Estrutura | Objetivo | campaign.objective | igual ao brief (ex.: OUTCOME_ENGAGEMENT) | id + valor |
| 1 | Estrutura | Status e erros | effective_status; ads_get_errors nos 3 níveis | ACTIVE quando ligada; lista de erros vazia | id + status + erros |
| 1 | Estrutura | Orçamento e duração | campaign.lifetime_budget ou daily_budget; adset.end_time | valor e fim iguais ao brief | valor bruto + data |
| 1 | Estrutura | Otimização | adset.optimization_goal; destination_type; promoted_object.page_id | CONVERSATIONS + WHATSAPP + página do brief | ids |
| 2 | Geo | Cidades incluídas | adset.targeting.geo_locations.cities / custom_locations | todas as cidades do brief presentes; nenhuma fora | lista comparada, contagem |
| 2 | Geo | Estado incluído | geo_locations.regions | vazio (ou só o permitido) | valor |
| 2 | Geo | Exclusões | excluded_geo_locations.regions | todos os estados do brief | contagem (ex.: 25 + DF) |
| 2 | Geo | Tipo de localização | geo_locations.location_types | home (moradores) | valor |
| 3 | Público | Idade e sexo | targeting.age_min/age_max; genders | iguais ao brief | valores |
| 3 | Público | Advantage+ público | targeting.targeting_automation.advantage_audience; targeting_optimization | 0 / none, se brief pedir fechado | valores |
| 3 | Público | Segmentação detalhada e públicos | flexible_spec; custom_audiences; excluded_custom_audiences | iguais ao brief (vazio se brief não pedir) | valores |
| 3 | Público | Tamanho estimado | adset estimate se disponível | dentro da faixa esperada para a rota | valor ou NÃO LIDO |
| 4 | Posicionamento | Plataformas e posições | targeting.publisher_platforms; facebook_positions; instagram_positions | iguais ao brief (automático ou lista) | valores |
| 5 | Criativo | Anúncios ativos | ads no conjunto com effective_status | quantidade e ids iguais ao brief | ids |
| 5 | Criativo | Conteúdo | creative object_story_spec: message, title, link_description, call_to_action.type, video_id/image_hash | texto e botão iguais ao aprovado; CTA WHATSAPP_MESSAGE | creative_id + campos |
| 5 | Criativo | Fatos comerciais | texto do criativo vs brief.fatos_permitidos | nenhum fato fora do brief | lista de fatos |
| 5 | Criativo | Diferença material | comparação entre criativos ativos | se mais de um: conceito/hook diferentes, não só cosmético | ids + resumo |
| 6 | Destino | Número e página | creative page_id; call_to_action.value (app_destination/whatsapp) | página do brief; destino WhatsApp da página | ids |
| 6 | Destino | Mensagem de boas-vindas | page_welcome_message se exposto | pergunta de cidade primeiro (filtro de rota) | valor ou NÃO LIDO |
| 7 | Sinais | Dataset/pixel | ads_get_datasets; ads_get_dataset_stats | dataset existe e recebe evento nos últimos 7 dias | id + contagem |
| 7 | Sinais | Conversões personalizadas | ads_get_customconversions | conforme brief | contagem |
| 7 | Sinais | Evento de otimização | adset.promoted_object.custom_event_type se houver | igual ao brief | valor |
| 8 | Aprendizado | Fase | adset.learning_stage_info | status e última edição significativa | valor + data |
| 8 | Aprendizado | Resultados previstos | orçamento / custo por conversa histórico | 50 resultados/semana alcançável ou RISCO declarado | conta explícita |
| 9 | Entrega | Leitura do dia | impressions, reach, spend, results, cost_per_result, frequency, cpm | dentro das faixas do brief | valores |
| 9 | Entrega | Anomalias | ads_insights_anomaly_signal | nenhuma anomalia aberta | valor ou NÃO LIDO |
| 10 | Governança | Aprovação humana | ledger/human_approval nos criativos | approved antes de ativar | registro |
| 10 | Governança | Edições após ativar | activity log ou learning_stage_info.last_sig_edit | nenhuma edição significativa após ligar | data |
| 10 | Governança | Dados pessoais | relatório e diário | nenhum telefone, nome de cliente ou conversa | conferência |

Regras de leitura:
- Tudo em horário BRT (UTC-3) com data.
- Item sem valor bruto = NÃO LIDO. Nunca OK por suposição.
- Benchmark e artigo de ajuda são referência, não veredito.
- Edição significativa (público, criativo, evento, novo anúncio, lance) reinicia aprendizado: qualquer correção proposta traz esse custo escrito.
