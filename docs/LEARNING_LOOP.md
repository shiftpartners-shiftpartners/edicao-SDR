# Ciclo de aprendizagem criativa

Este ciclo conecta edição e mídia sem transformar correlação em certeza. A unidade de aprendizagem é a variante identificada por `creative_id`, não o nome informal do arquivo.

## Fluxo

1. **Hipótese:** registrar qual mudança deve produzir qual efeito e por quê.
2. **Produção:** alterar uma variável principal sempre que for operacionalmente possível.
3. **QC:** provar que o render corresponde ao plano e está apto a testar.
4. **Handoff:** entregar `creative_id`, objetivo, destino e versão junto com o arquivo.
5. **Observação:** anexar janela, gasto, impressões, alcance e eventos relevantes.
6. **Leitura:** comparar somente observações minimamente compatíveis.
7. **Decisão humana:** `escalar`, `iterar`, `pausar` ou `inconclusivo`.
8. **Próxima rodada:** transformar a decisão em nova hipótese, sem sobrescrever o histórico.

## Estados

| Estado | Significado |
|---|---|
| `draft` | hipótese ou cadastro incompleto |
| `qc_pending` | render existente, ainda não aprovado |
| `approved` | apto para handoff humano |
| `observing` | em janela de observação |
| `decided` | decisão humana registrada |
| `archived` | preservado, fora da rodada ativa |

## Quatro decisões permitidas

- `escalar`: manter a tese e ampliar com controle humano da operação de mídia.
- `iterar`: preservar o aprendizado e mudar uma dimensão definida.
- `pausar`: retirar da rodada ativa, sem apagar o registro.
- `inconclusivo`: dados, janela ou comparabilidade insuficientes.

## Antirrepertório

- hook que promete algo que a peça não entrega;
- demonstração sem legibilidade no celular;
- crop que elimina informação essencial;
- conceitos cosmeticamente diferentes cadastrados como novos;
- leitura baseada em CTR, CPM ou custo isolado sem relação com o objetivo;
- comparação entre períodos, públicos, orçamento ou placements materialmente diferentes sem ressalva.

## Regra de saturação

Fadiga não é inferida por sensação. Registrar a hipótese quando houver deterioração ao longo do tempo e verificar mudanças concorrentes: frequência, público, oferta, placement, orçamento, sazonalidade, atendimento e mensuração.
