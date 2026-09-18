# QC de Criativos — O Segredo da Roça

O QC deve avaliar o render final e separar falhas técnicas de falhas criativas e de verdade comercial.

## Técnico

- arquivo abre e reproduz até o fim;
- duração e proporção estão corretas;
- não há frame preto acidental na abertura;
- não há congelamento ou frame corrompido;
- crop não corta produto, rosto, texto ou informação essencial;
- texto está dentro de área segura;
- legenda está sincronizada;
- áudio não clipa e fala permanece inteligível;
- codec/container são compatíveis com o destino;
- render corresponde à versão registrada no EDP.

## Criativo

- o primeiro segundo tem uma razão visual ou verbal para continuar;
- hook, conceito e execução estão coerentes entre si;
- cada beat acrescenta algo;
- a peça não demora para chegar ao produto ou ideia central;
- texto em tela é legível em celular;
- CTA está claro quando a peça exige CTA;
- ritmo corresponde ao material e ao placement;
- a variante é realmente distinta da anterior quando foi registrada como novo conceito.

## Verdade e governança

- preço, promoção, prazo e garantia foram confirmados;
- nenhuma prova social foi fabricada;
- nenhuma avaliação, número ou estatística foi inferida;
- imagens não sugerem característica que o produto não possui;
- ausência de dado continua marcada como ausência;
- aprovação humana está registrada antes da saída para mídia.

## Padrão OSDR (`docs/PADRAO_EDICAO_OSDR.md`)

- comida, produto ou movimento no segundo zero; nada de logo, "oi pessoal" ou tela preta;
- cortes a cada 2–3 s no início e 3–5 s no meio; nenhum plano parado acima de 3 s;
- legenda em blocos de 3–5 palavras, sincronizada, sem travessão, fora de rosto/produto;
- som de produto em pelo menos um momento; trilha como cama;
- fechamento em pergunta, frame congelado com texto curto ou convite seco;
- duração e formato dentro do template (`scripts/qc_render.py --template`);
- capa escolhida a dedo, legível em miniatura.

## Verdade comercial OSDR

- preço, frete, prazo, brinde, garantia, rota e kit só com fonte autorizada (Lei Comercial vigente, Base Operacional, decisão registrada);
- prazo sempre na fórmula aprovada, nunca dia/hora;
- kit pausado não aparece; rota fora da lista vigente não aparece;
- uso de IA generativa e alterações significativas registrados no ledger.

## Score opcional

```yaml
adherence: null
hook_strength: null
pacing: null
visual_quality: null
legibility: null
watchability: null
truth_compliance: null
distinctiveness: null
overall: null
feedback: ""
```

Uma falha grave de verdade, crop ou legibilidade reprova a versão independentemente da média.

## Gate de aprendizagem

QC aprovado significa “tecnicamente apto a testar”, não “provavelmente vencedor”. Resultado de mídia é registrado separadamente e nunca retroage para apagar falhas de verdade ou compliance.