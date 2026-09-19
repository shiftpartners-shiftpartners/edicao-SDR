---
name: auditar-campanha-meta
description: Audita uma campanha Meta Ads viva contra o brief da operação usando o agente auditor-de-trafego-meta e o checklist fixo de docs/CHECKLIST_AUDITORIA_META.md. Use antes de ligar, em cada check-in diário, antes de editar qualquer coisa e quando a operação pedir "auditoria", "confere o anúncio", "está certo?".
---

# Auditar campanha Meta

## Quando usar
- Antes de ativar uma campanha nova.
- Em cada leitura diária de campanha em teste.
- Antes de qualquer edição significativa (público, criativo, orçamento, evento, novo anúncio).
- Quando a operação perguntar se a campanha está certa.

## Entradas
1. `campaign_id` e `ad_account_id`.
2. Brief da campanha em YAML (`BRIEF_CAMPANHA_<nome>.yaml`) com: objetivo, página, destino (WhatsApp/site), orçamento e duração, geo incluída (lista de cidades e raios), geo excluída, idade, sexo, posicionamentos, criativos aprovados (ids), fatos comerciais permitidos, critério de sucesso por faixa.
3. `client_conversation_id` da sessão Meta.

## Passos
1. Se não houver brief, crie o YAML a partir das ordens escritas da operação (citando data e mensagem) antes de auditar. Hipótese é marcada `provisorio: true`.
2. Rode o agente `auditor-de-trafego-meta` com campanha, conta, brief e conversation id.
3. Leia o relatório. Se algum bloco estiver `NÃO LIDO` por ferramenta ausente, registre como bloqueio técnico com ferramenta, ação, erro e substituto.
4. Registre no `LOG.md` do lote: data/hora BRT, id da campanha, nome do relatório, número de FALHA/RISCO/NÃO LIDO.
5. Entregue à operação em blocos curtos: três falhas mais graves, o que não fazer agora, próxima leitura. Sem links a menos que pedido.

## Saída
- `AUDITORIA_CAMPANHA_<id>_<AAAA-MM-DD>_<HHMM>.md` na pasta de trabalho do lote (versionado, nunca sobrescreve).
- Linha no `LOG.md`.

## O que esta skill não faz
- Não edita, ativa, pausa ou apaga nada na Meta.
- Não decide orçamento nem criativo: descreve o parâmetro e quem aprova.
- Não usa benchmark como veredito.
