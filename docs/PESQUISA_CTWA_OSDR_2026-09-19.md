# Pesquisa aplicada: como vender por anúncio de mensagem (CTWA) para O Segredo da Roça

Data: 19/09/2026. Ferramentas: Central de Ajuda da Meta (ferramenta de leitura), busca e leitura web. Nenhuma escrita na Meta.
Cobertura: o proxy bloqueou quase todos os domínios de terceiros; para esses só entrou o trecho do buscador, marcado "RELATO (snippet, não aberto)". Nenhum tópico do Reddit pôde ser aberto nem apareceu na busca. Todo conteúdo OFICIAL foi lido na íntegra pela ferramenta da Meta.
Legenda: OFICIAL = Meta lida na íntegra. OFICIAL (snippet) = página Meta não aberta. RELATO = praticante, agência, fornecedor. INFERÊNCIA = dedução a partir das fontes e dos fatos do cliente.

## 1. Resumo executivo

1. Estancar o vazamento geográfico: desmarcar "Alcançar mais pessoas com probabilidade de responder" (vem ligado por padrão ao escolher cidade), usar "somente cidade atual" nas cidades da rota, excluir cidades vizinhas fora da rota e travar 45 a 65 como controle (por padrão idade é só sugestão). A Meta admite por escrito que vazamento de localização acontece; isso reduz, não zera, os 64% fora da rota.
2. Filtrar antes do clique: rota, dia de entrega e "12x R$ 39,90" na primeira linha do texto e na imagem; perguntas prontas do template "Iniciar conversa" que separam "moro em SP/Grande SP" de "moro fora"; a Yara pergunta cidade ou CEP como primeira ação. Cada conversa iniciada é cobrada, então o filtro precisa estar no criativo, não só no bot.
3. Mandar sinal de compra pela CAPI for Business Messaging (a operação já usa Cloud API): guardar ctwa_clid do webhook, enviar Purchase com action_source business_messaging quando a vendedora marcar "pago". A Meta exige 10 compras em 30 dias, rotuladas até 7 dias após o clique, para liberar "maximizar compras em mensagens".
4. Manter objetivo Engajamento e otimização Conversas até ter esse histórico: é a configuração que a Meta marca como recomendada e é o evento mais frequente (única chance de chegar perto de 50 resultados por semana com R$ 170 a 350).
5. Uma campanha, um conjunto, 3 a 5 criativos materialmente diferentes; nada de vários conjuntos com esse orçamento.
6. Orçamento vitalício só se for usar agenda de horários; caso contrário diário. Com R$ 170 por semana e R$ 4 a 9 por conversa, dá 19 a 43 conversas; só perto de R$ 350 por semana e custo até R$ 7 chega a 50.
7. Não editar nada por 7 dias após cada mudança significativa (segmentação, criativo, evento, novo anúncio).
8. Benchmarks brasileiros são relatos de fornecedores, sem metodologia; usar só como faixa. O cliente já está na faixa baixa (R$ 4 a 9).

## 2. Achados por pergunta

### Estrutura de campanha com orçamento pequeno

| Prática | O que diz | Fonte | Tipo | Aplica? |
|---|---|---|---|---|
| Objetivo Engajamento | "Entrega a pessoas mais propensas a responder para iniciar uma conversa (recomendado)". Tráfego só manda ao destino; Vendas para "mais propensas a comprar". | help/1192884166182156 | OFICIAL | Sim, manter |
| Vendas com destino mensagem | "Escolha Vendas se quiser aumentar vendas no WhatsApp". | help/672411877425804, help/447934475640650 | OFICIAL | Só depois de compras via CAPI |
| Maximizar compras em mensagens | Exige 10+ eventos de compra em 30 dias (app WhatsApp Business ou CAPI), conversas vindas de CTWA, rotuladas até 7 dias após o clique; rodar 7+ dias. | help/1214599109289826 | OFICIAL | Ainda não (dataset nunca recebeu compra) |
| Fase de aprendizado | Sai com cerca de 50 resultados na semana após a última edição significativa. | help/112167992830700 | OFICIAL | Sim |
| Aprendizado limitado | Causas: público pequeno, orçamento baixo, evento infrequente, muitos anúncios. Correções: combinar conjuntos, ampliar público, subir orçamento, evento mais frequente. | help/269269737396981 | OFICIAL | 1 campanha, 1 conjunto, evento = conversa |
| Edições que reiniciam | Segmentação, criativo, evento, novo anúncio, pausa de 7+ dias, lance; orçamento só se variação grande. | help/316478108955072 | OFICIAL | Agrupar mudanças num momento só |
| CBO vs ABO | CBO para 2+ conjuntos; ABO para controle por conjunto. | help/153514848493595, help/458847204894307 | OFICIAL | Com 1 conjunto é indiferente |
| Diário vs vitalício | Diário pode gastar até 75% acima em alguns dias; vitalício distribui no período e permite agenda. | help/190490051321426, help/1844835042445690, help/343242619559352 | OFICIAL | Diário por padrão |
| Orçamento mínimo com meta de custo | Diário ≥ 5x a meta. | help/203183363050448 | OFICIAL | Não usar meta de custo agora |
| Conta do cliente | R$ 170 a 350 ÷ R$ 4 a 9 = 19 a 88 conversas por semana; 50 só com ≥ R$ 325 a ≤ R$ 6,50. | cálculo | INFERÊNCIA | Aceitar limitado ou R$ 350 fixo |

### Segmentação para entrega local

| Prática | O que diz | Fonte | Tipo | Aplica? |
|---|---|---|---|---|
| Quem a localização alcança | "Pessoas que moram lá, estiveram recentemente ou vão com frequência." Sem menu "somente moradores" no texto atual. | help/202297959811696 | OFICIAL | Assumir que visitante entra |
| Vazamento admitido | "Precisão total não pode ser garantida. Você pode receber mensagens ou leads de fora." | help/202297959811696 | OFICIAL | Explica parte dos 64% |
| "Alcançar mais pessoas com probabilidade de responder" | Vem marcado por padrão ao escolher cidade; inclui quem pesquisou, interagiu, tem amigos ou mora perto. Desligar se quer só quem mora, esteve ou frequenta. | help/726389026372510, help/365561350785642 | OFICIAL | Verificar e desmarcar |
| Cidade fechada vs raio | Ao escolher cidade, "somente cidade atual" ou raio; raio inclui tudo dentro dele. | help/365561350785642 | OFICIAL | Cidade atual para a rota |
| Exclusões | Quem mora em local incluído pode ver o anúncio visitando local excluído. | help/365561350785642 | OFICIAL | Excluir cidades limítrofes fora da rota |
| Idade é sugestão por padrão | "Por padrão idade e gênero são sugestões, exceto idade mínima"; travar em "limitar ainda mais o público". | help/151999381652364 | OFICIAL | Confirmar 45 a 65 como controle |
| Público estreito custa mais | "Custo por resultado pode ser pelo menos o dobro". | help/1098451937465750 | OFICIAL | Aceitar em troca de conversas na rota |
| Causa número 1 no Brasil | Expansão de localização é "disparado a principal causa de leads fora da cidade". | igorfortaleza.com.br | RELATO (snippet) | Sim |

### Criativo para CTWA e público 45 a 65

| Prática | O que diz | Fonte | Tipo | Aplica? |
|---|---|---|---|---|
| Deixar claro que abre chat | Criativo deve dizer que clicar abre conversa; CTA Enviar mensagem; mix de vídeo e imagem; boas-vindas e respostas rápidas adaptadas. | help/269324800441478 | OFICIAL | Sim |
| Duração e som | Feed abaixo de 15 s; Stories abaixo de 10 s; marca e mensagem nos 3 primeiros segundos; projetar para som desligado. Som ligado teve 2,25x mais CTR no CTA. | help/188534925073536 | OFICIAL | Sim; legenda obrigatória |
| Quantos criativos | Até 10 por conjunto, ficar com os 5 melhores, testar 4+ dias; aprendizado alerta contra volume alto. | help/188534925073536, help/112167992830700 | OFICIAL | 3 a 5 com este orçamento |
| Carrossel barato | Se vídeo é caro, carrossel; legendas automáticas. | help/1991663177718491 | OFICIAL | Testar carrossel das peças + brinde |
| Advantage+ criativo | Gera variações de mídia e texto. | help/376490293773516, help/1176714013185487 | OFICIAL | Testar com melhorias visuais desligadas |
| Conceitos, não variações | 4 a 6 conceitos diferentes por conjunto; acima de 7 ativos CPM sobe. | chatterbuzz, segwise, adscale | RELATO (snippet) | Sim, no princípio |
| Público 65+ | Texto e visual simples, fato específico, legenda e CTA gráfico. | generationsnow, billo | RELATO (snippet) | Sim |
| Preço na dobra | Sem fonte específica de CTWA. Dedução: preço e rota no primeiro quadro reduzem clique curioso e fora da rota. | cálculo | INFERÊNCIA | Testar A/B |
| Template "Iniciar conversa" | Saudação e até 4 perguntas sugeridas que a pessoa toca. | help/447934475640650; manychat, respond.io, blip | OFICIAL + RELATO | Sim |

### Filtro de rota antes do clique

| Prática | O que diz | Fonte | Tipo | Aplica? |
|---|---|---|---|---|
| Segmentação vaza, filtro vai no criativo e no bot | Meta: "você pode receber mensagens de fora". | help/202297959811696 | OFICIAL | Sim |
| Rota e frete na primeira linha | Promessa do anúncio define quem chega; lead desalinhado "clicou por engano". | pontocomaudio, renovedigital | RELATO (snippet) | Sim |
| Bot pergunta cidade primeiro | Chatbot pergunta cidade e necessidade antes de ofertar; tag; humano; follow-up. | gestor-de-trafego, chatplusbr | RELATO (snippet) | Sim |
| Perguntas prontas que separam rota | 2 dos 4 botões: "Moro em SP/Grande SP (entrega sábado)" e "Moro fora de SP (Correios, pagamento antecipado)"; a escolha chega como texto no webhook e vira rótulo. | dedução a partir do template oficial | INFERÊNCIA | Sim |
| 7 erros de funil | Público "todo mundo"; primeira mensagem confusa; mandar fechar no site perde 50 a 70%; cobrar Pix no fluxo. | devzapp | RELATO (snippet) | Sim, exceto Pix no bot |

### Sinal de compra (CAPI for Business Messaging)

| Prática | O que diz | Fonte | Tipo | Aplica? |
|---|---|---|---|---|
| Pré-requisitos | App de desenvolvedor; acesso avançado a whatsapp_business_management e whatsapp_business_manage_events; Ads Management Standard Access; Cloud API. | developers: conversions-api/business-messaging | OFICIAL | Sim, exige desenvolvedor |
| ctwa_clid | Obrigatório para enviar eventos; vem no webhook (objeto referral) da Cloud API. | mesma fonte; github typebot.io #1906 (aberto) | OFICIAL + RELATO | Yara grava na primeira mensagem |
| Payload | event_name purchase, event_time até 7 dias no passado, action_source business_messaging, messaging_channel, user_data do canal, custom_data value/currency, event_id. | developers: parameters/server-event | OFICIAL | Sim |
| Elegibilidade | 10+ compras em 30 dias de conversas CTWA, rotuladas até 7 dias após o clique. | help/1214599109289826 | OFICIAL | Sim |
| Resultado prometido | Otimizar por compras em mensagens: em média 10% menos custo por compra que por conversa. | business.whatsapp.com | OFICIAL (snippet) | Ganho modesto |
| ctwa_clid pode faltar | Tópico "ctwa_clid missing from referral data"; relato de que precisa atribuição habilitada no WhatsApp Business. | comunidade dev Meta; whapi | RELATO (snippet) | Verificar no primeiro teste |
| Janela de 7 dias vs entrega de sábado | Clique de sexta à noite pode cair na entrega do sábado seguinte (8+ dias) e não contar. Enviar também Lead "na rota" no dia do clique. | cálculo | INFERÊNCIA | Registrar data do clique e da confirmação |

### Remarketing

| Prática | O que diz | Fonte | Tipo | Aplica? |
|---|---|---|---|---|
| Públicos de engajamento | Vídeo, Página, Instagram etc., até 365 dias; origem de lookalike. WhatsApp não é fonte nativa. | help/1090330204367211, help/744354708981227 | OFICIAL | Vídeo e Página/IG sim |
| Público de vídeo | Se o vídeo foi reaproveitado de post, o público reflete só o post. Subir a mídia direto no anúncio. | help/1099865760056389 | OFICIAL | Sim |
| Lista de clientes | CSV com telefone, hash local; portfólio empresarial; gera lookalike. | help/170456843145568 | OFICIAL | Compradores viram lista (LGPD; nunca no repositório) |
| Lookalike mínimo | 100 pessoas do mesmo país; recomendado 1.000 a 5.000. | jonloomer | RELATO (snippet) | Quando houver 100+ compradores na rota |
| Exclusão de quem já conversou | Excluir engajados da Página para prospecção é uso previsto. | help/221146184973131 | OFICIAL | Excluir compradores e "fora da rota" da aquisição |

### Erros comuns (praticantes)

- Expansão de localização ligada (igorfortaleza). Público "todo mundo" e primeira mensagem confusa (devzapp). Tratar "bom dia" perdido como lead (pontocomaudio). Medir por custo por conversa em vez de custo por compra (orai). Objetivo Tráfego (egrow). Criativo único e fadiga em 2 a 3 semanas (segwise). Repasse de impostos em 2026, +12% no custo (aisensy, messagecentral; não verificado na Meta). Cobrança de respostas via API a partir de outubro de 2026, R$ 0,035 cada fora da janela grátis de 72 h de CTWA (mobiletime, ecommercebrasil; snippet). Todos RELATO (snippet). Reddit: não coberto.

### Benchmarks (todos RELATO, sem metodologia aberta)

| Métrica | Valor relatado | Fonte |
|---|---|---|
| Custo por conversa CTWA Brasil | R$ 3 a 40 por vertical; moda/beleza R$ 3 a 8 | messagecentral (2026) |
| Conversão WhatsApp vs e-commerce | até 6x; Hering 20%; supermercados até 27% | Chat Commerce Report 2025 (OmniChat), grandes varejistas |
| Conversão média e-commerce BR | 1,65% | prax (2025) |
| Claims da Meta | 79% relatam ROAS 1,5x; multi destino 9% menos custo por mensagem | Meta (snippet) |
| Conversa em venda para PME local | nenhum benchmark aberto | lacuna |

## 3. Contradições entre fontes

1. Objetivo: Engajamento "recomendado" para mensagem, mas Vendas "se quiser aumentar vendas". O que importa é a meta de desempenho: Engajamento + Conversas hoje; Compras em mensagens quando elegível.
2. "Somente moradores": blogs de 2026 dizem que só resta "morando ou recentemente em"; o texto oficial atual não mostra seletor. Assumir que não há filtro de morador puro.
3. Quantidade de criativos: oficial até 10 (ficar com 5); Andromeda 4 a 6; aprendizado pede pouco volume. Com R$ 350 por semana, 3 a 5.
4. CBO vs ABO: indiferente com um conjunto.
5. Estático vs vídeo: só teste resolve.
6. Métrica "novos contatos de mensagem" tem duas definições oficiais (help/948786449503922 vs help/200955703676800). Não usar para comparar canais.

## 4. O que NÃO fazer

- Não ligar "Alcançar mais pessoas com probabilidade de responder" nem Advantage+ público enquanto o problema for gente fora da rota.
- Não migrar para Vendas ou compras em mensagens antes de 10 compras rotuladas em 30 dias.
- Não abrir vários conjuntos com R$ 170 a 350 por semana.
- Não editar segmentação, criativo ou evento em dias separados; agrupar e esperar 7 dias.
- Não usar Tráfego nem Alcance.
- Não reaproveitar vídeo de post existente se quiser público de vídeo; subir direto.
- Não deixar bot ou vendedora prolongar conversa fora da rota sem oferta clara ou encerramento.
- Não usar meta de custo por resultado.
- Não subir lista de clientes sem base legal; nunca telefones no repositório.
- Não usar benchmark de fornecedor como meta interna.

## 5. Plano de teste de 2 semanas

Premissas: uma campanha Engajamento, um conjunto, Conversas, WhatsApp, R$ 50 por dia (R$ 350 por semana) ou o máximo aprovado; aprovação humana antes de ligar. Todas as mudanças entram no dia 1 (um reset só).

Semana 1: vazamento e filtro pré-clique.
- Dia 1: desmarcar expansão de localização; cidades da rota em "somente cidade atual"; excluir cidades limítrofes fora da rota; 45 a 65 como controle; excluir "idade desconhecida no WhatsApp" se Status estiver ativo; lista de compradores e de "fora da rota" como exclusão (se houver base legal).
- 3 criativos materialmente diferentes: (a) estático 4:5 com kit, "12x R$ 39,90", "entrega sábado em SP e Grande SP"; (b) vídeo 10 a 15 s com legenda grande e rota nos 3 primeiros segundos; (c) carrossel peças + 4 tigelas, último card com rota e frete. Texto principal com rota e dia de entrega na primeira linha.
- Template "Iniciar conversa": saudação repete a oferta; 4 perguntas: "Moro em SP/Grande SP, quero entrega no sábado", "Moro fora de SP, quero pelos Correios", "Quero ver as peças", "Como funciona o pagamento na entrega?".
- Yara: primeira ação pergunta cidade ou CEP; fora da rota recebe oferta Correios e rótulo fora_rota; na rota vai para vendedora com rótulo na_rota.
- Engenharia em paralelo: gravar ctwa_clid e hora do clique na primeira mensagem; vendedora marca "pago" com valor; enviar Lead (na_rota) no dia e Purchase quando pago; validar no Gerenciador de Eventos.
- Hipóteses: H1 conversas na rota de 36% para ≥ 60%; H2 custo por conversa ≤ R$ 9 com público mais estreito; H3 custo por conversa na rota cai ≥ 30%; H4 ≥ 90% das primeiras mensagens de anúncio trazem ctwa_clid.
- Nada de edição entre dia 1 e dia 7.

Semana 2: criativo e sinal.
- Dia 8: manter os 2 melhores por custo por conversa na rota; trocar o pior por 1 conceito novo na mesma edição.
- Se H1 falhou (< 50% na rota): preço e rota maiores no primeiro quadro; saudação começando por "Entregamos só em SP e Grande SP aos sábados".
- Sinal: contar compras via CAPI dentro de 7 dias do clique; meta 10 em 30 dias.
- Dia 14: custo por conversa total e na rota; % na rota; conversa na rota em venda; compras no dataset; status de aprendizado; frequência (alerta > 3 em 7 dias).
- Dia 15: se ≥ 10 compras e ≥ 50 conversas por semana, planejar migração para compras em mensagens; senão, manter Conversas mais 2 semanas e revisar criativos.

## 6. Fontes oficiais lidas na íntegra (facebook.com/business/help/<id>, acessadas 19/09/2026)

447934475640650 · 1192884166182156 · 672411877425804 · 269324800441478 · 1214599109289826 · 112167992830700 · 269269737396981 · 316478108955072 · 1707952432550214 · 458847204894307 · 153514848493595 · 343242619559352 · 190490051321426 · 1844835042445690 · 340985466050775 · 203183363050448 · 365561350785642 · 202297959811696 · 726389026372510 · 151999381652364 · 1665333080167380 · 1098451937465750 · 188534925073536 · 1991663177718491 · 817989058548892 · 376490293773516 · 1176714013185487 · 287043621933356 · 1816962591668838 · 1090330204367211 · 744354708981227 · 221146184973131 · 1099865760056389 · 170456843145568 · 341425252616329 · 598014914327226 · 948786449503922 · 200955703676800 · 780327487508857. Developers: marketing-api/conversions-api/business-messaging e conversions-api/parameters/server-event.

Relatos (só snippet, domínio bloqueado): egrow, asisteclick, aisensy, messagecentral, devzapp, igorfortaleza, jonloomer, adenslab, tacticlab, chatterbuzz, segwise, adscale, superscale, adsuploader, dataslayer, kecg, generationsnow, billo, manychat, blip, respond.io, orai, sanuker, abcsales, woztell, whapi, comunidade dev Meta, doubletick, pontocomaudio, renovedigital, gestor-de-trafego, chatplusbr, hsgmarketing, sleekflow, ecommercebrasil, omni.chat, prax, mobiletime, YouTube (2 vídeos). Aberto e lido: github.com/baptisteArno/typebot.io/issues/1906.

Lacunas: Reddit não coberto; sem estudo de conversão de perguntas prontas; sem benchmark aberto de conversa em venda para PME local; "10% menos custo por compra" e faixas brasileiras vistos só em trechos.
