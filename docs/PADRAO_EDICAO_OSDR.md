# Padrão editorial de vídeo — O Segredo da Roça

Classificação: **padrão interno vigente (V1, mai/2026)**. É prática editorial da casa, não regra da Meta. Origem: skill operacional `osdr-edicao-video` do operador; aqui fica a versão de referência para agentes e QC deste repositório. Atualizar por nova versão datada, não por edição silenciosa.

## Regra central

Vídeo do OSDR precisa **prender em 2 segundos**, **reter até o fim** e **deixar saliva ou saudade**. Sem isso não sai da bancada.

## Os cinco pontos críticos

### 1. Gancho nos primeiros 2 segundos
Serve: comida pronta saindo da panela (vapor, brilho, cor), mão no cabo da panela quente, close em movimento, som do produto antes da imagem, pergunta seca em texto.
Não serve: logo, "oi pessoal", tela preta, apresentação de quem fala, ambiente vazio.

### 2. Ritmo de corte
Corte a cada 2 a 3 s no início; 3 a 5 s no meio; corte no auge sem fechar tudo. Câmera parada mais de 3 s sem nada acontecer: corta.

### 3. Duas camadas de áudio
Trilha em alta da plataforma em volume médio-baixo (cama). Som do produto em destaque: borbulha, óleo na cebola, faca no alho, água, tampa, colher de pau, comida servida. Voz alta e limpa.

### 4. Legenda dinâmica obrigatória (quando há fala)
Blocos de 3 a 5 palavras, quebra que respeita a ideia. Sans-serif pesada, branco com sombra ou amarelo OSDR em palavra-chave. Terço inferior, nunca sobre rosto, panela ou comida. Sincronizada com a fala. Sem travessão. Ferramenta: `scripts/caption_segments.py`.

### 5. Fechamento que segura
Bons: comida no prato com garfo entrando, pergunta sem resposta, frame congelado com texto curto, convite seco ("Comenta EU QUERO").
Maus: "obrigado por assistir", logo gigante, "siga, curta, compartilhe", música acabando sozinha.

## Visual

- Formato 9:16, mínimo 1080×1920, 30 fps. Feed pago pode usar 4:5.
- Paleta quente: preto fosco do barro, dourado da comida, vermelho-tijolo do refogado, madeira, louça branca quente, verde da couve. Evitar azul saturado, cinza neutro, rosa, roxo.
- Planos: close extremo (textura) na abertura e no auge; plano detalhe para vender o produto; plano médio para contexto; plano aberto raramente.
- Transições só quando somem com algo no quadro: match cut, whip pan, corte seco na batida, vapor cobrindo. Sem fade, wipe, glitch, efeito "mágico".
- Capa: frame forte escolhido a dedo, texto de 3 a 6 palavras, cor saturada, sem logo gigante, legível em miniatura.

## Curva emocional

Tensão/curiosidade (0–3 s) → construção (3–10 s) → auge (10–13 s) → resolução curta (último segundo). Não distribuir tensão por igual.

## Templates por formato

Definidos em `templates/osdr-formats.json` e aplicados pelo QC (`scripts/qc_render.py --template <nome>`).

| Template | Objetivo | Duração | Estrutura |
|---|---|---|---|
| `reel15` | apetite | 12–16 s | comida saindo (0–2) · servida (2–5) · textura (5–9) · garfo (9–13) · frase final (13–15) |
| `reel30` | educacional | 25–32 s | gancho (0–3) · problema (3–10) · resolução (10–22) · prova (22–27) · convite (27–30) |
| `tiktok` | alcance | 8–16 s | imagem inesperada (0–1) · pergunta (1–3) · resposta em 2–3 cortes (3–8) · auge (8–12) · pergunta sem resposta + congela |
| `meta-ad` | conversão paga | 5–10 s | gancho + promessa em texto (0–1,5) · produto em ação (1,5–4) · resultado (4–6) · CTA + frame congelado (6–9) |
| `meta-ad-feed` | conversão paga em feed 4:5 | 5–15 s | mesma estrutura do `meta-ad`, enquadramento 4:5 |
| `nano` | volume | 5–8 s | um plano forte por segundo |
| `story` | ação direta | 1–5 s por card | texto curto, fundo escuro ou sépia, sequência de 4 a 6 cards |

Anúncio Meta: texto na tela obrigatório, logo pequeno (até 8% do quadro), CTA na tela final, último frame pronto para virar miniatura.

## Verdade comercial no vídeo

Preço, prazo, frete, brinde, garantia, rota, kit disponível e prova social só entram com fonte autorizada (Lei Comercial vigente, Base Operacional ou decisão registrada). Prazo de entrega é sempre a fórmula aprovada, nunca dia/hora. Kits pausados não aparecem. O agente `guardiao-da-verdade` confere antes do QC e do handoff.

## Sinais de alarme (reprova na hora)

- preço, prazo ou oferta não confirmados;
- produto pausado ou rota fora da lista vigente;
- travessão na legenda;
- texto que poderia ser de qualquer marca;
- começa com "oi pessoal" ou tela preta;
- fala sem legenda;
- termina com "siga, curta, compartilhe".

## Última pergunta

"Você assistiria até o fim sem pular?" Se a resposta for "talvez", refaz.
