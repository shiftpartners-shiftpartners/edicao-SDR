# Contrato de medição e handoff

Este repositório não gerencia campanhas. Ele entrega identidade e contexto suficientes para que mídia e mensuração devolvam observações utilizáveis.

## Chave de junção

`creative_id` é a chave obrigatória entre registro criativo, nome do render, handoff para mídia, observação de performance e decisão humana.

## Campos mínimos do handoff

- `creative_id` e `asset_filename`;
- conceito, hook, execução, formato e versão;
- produto ou linha;
- hipótese e variável principal alterada;
- objetivo de mídia informado pelo responsável;
- data e pessoa que aprovou o handoff.

## Campos mínimos da observação

- período em UTC ou timezone explícito;
- moeda;
- gasto, impressões e alcance quando disponíveis;
- cliques, conversas iniciadas, leads qualificados, compras e valor, conforme o funil real;
- fonte do dado;
- mudanças concorrentes e limitações;
- decisão humana e justificativa.

## Semântica de ausência

- `null`: não disponível ou não aplicável;
- `0`: medido e igual a zero;
- campo omitido: registro inválido quando o schema o exige.

Nunca substituir ausência por zero.

## Limites

- Uma observação não prova causalidade.
- Métricas de plataforma e CRM podem divergir por janela, identidade e atribuição.
- Conversa iniciada não é compra.
- Compra devolvida à Meta não substitui conferência do sistema de pedidos.
- Mudança simultânea de criativo, público, orçamento, oferta ou atendimento reduz a força da comparação.
