# Pipeline de Produção — O Segredo da Roça

Este documento traduz padrões de edição agêntica para um fluxo simples, auditável e compatível com operação real.

A referência principal é a separação de papéis vista em `agentic-video-editor` e o uso de um plano de edição reproduzível adotado pelo ForwrdCut. Não copiamos a aplicação inteira; aproveitamos o padrão arquitetural.

## Pipeline-base

```text
Material bruto
  ↓
Preprocessamento
  ↓
Inventário de cenas e falas
  ↓
Direção criativa
  ↓
Edit Decision Plan (EDP)
  ↓
Refino de cortes
  ↓
Render
  ↓
QC técnico + criativo + verdade
  ↓
Aprovação humana
  ↓
Entrega
```

## Papéis

### 1. Preprocessador
Transforma arquivos brutos em informação utilizável.

Saídas mínimas:
- metadados de vídeo e áudio;
- duração;
- orientação;
- resolução;
- cenas detectadas;
- transcrição quando houver fala;
- frames representativos/contact sheet;
- erros de mídia encontrados.

Não toma decisão criativa.

### 2. Diretor
Recebe briefing + inventário e monta a intenção da peça.

Decide:
- conceito;
- hook;
- ordem dos beats;
- trechos candidatos;
- duração-alvo;
- CTA aprovado;
- uso de texto, legenda e reframe.

Saída: EDP revisável antes do render.

### 3. Refinador de corte
Aperta início e fim de cada trecho para remover sobra, silêncio, entrada atrasada e saída frouxa.

Pode usar automação, mas não deve destruir momentos importantes de fala ou demonstração.

### 4. Editor/Renderer
Executa o plano. FFmpeg é a base preferida.

O renderer não decide tese, claim ou mensagem comercial.

### 5. Reviewer/QC
Avalia o render pronto, não apenas o plano.

Dimensões sugeridas:
- aderência ao brief;
- força do hook;
- pacing;
- legibilidade;
- qualidade visual;
- enquadramento/crop;
- áudio;
- aderência de claims;
- CTA;
- watchability;
- diferença material versus outras variantes.

A nota automática é apoio, não aprovação final.

## Regra de retry

Se um render falhar no QC, a correção volta ao nível responsável pelo problema.

Exemplos:
- crop ruim → reframe/editor;
- hook fraco → diretor;
- claim não aprovado → diretor/brief;
- silêncio sobrando → refinador;
- codec/áudio quebrado → renderer.

Evitar reprocessar toda a peça se apenas um beat estiver ruim.

## Gate humano

Antes de qualquer saída para mídia, confirmar:
- produto e oferta;
- texto final;
- preço/prazo/garantia quando existirem;
- identidade visual;
- variante escolhida;
- destino correto da peça.

## Estado executável

Cada papel acima tem um subagente em `.claude/agents/` e um script: inventário (`media_probe.py`, `contact_sheet.py`), refino e conversão (`edp_to_render_plan.py`), render (`render_plan.py`), legenda (`caption_segments.py`), QC técnico por template (`qc_render.py --template`), diversidade (`diversity_check.py`) e handoff (`handoff_pack.py`). O mapa está em `docs/MAQUINA_DE_EDICAO.md`; limites em `docs/SETUP.md`. Não existe orquestrador automático: a passagem entre etapas é decisão do operador.

## Regra de simplicidade

Só adicionar um novo agente, etapa ou ferramenta quando uma falha operacional real justificar.

Se FFmpeg + inventário + EDP + revisão humana resolverem, não adicionar outra camada.