# Workflow operacional — O Segredo da Roça

## Entrada

Receber apenas o necessário para a peça:

- material bruto;
- objetivo;
- produto/linha;
- placement;
- duração desejada;
- oferta e CTA aprovados, quando existirem;
- restrições de marca;
- referência visual, se houver.

## Etapa 1 — Inventário

Rodar `scripts/media_probe.py` e gerar contact sheets dos vídeos candidatos com `scripts/contact_sheet.py`.

O material deve ser inspecionado antes de qualquer decisão de corte.

Antes de decidir, ler `docs/PADRAO_EDICAO_OSDR.md` e escolher o template em `templates/osdr-formats.json`.

## Etapa 2 — Arquitetura criativa

Definir:

- conceito;
- hook;
- execução;
- formato;
- duração;
- beats principais.

Quando houver múltiplas peças, montar a matriz de variantes antes de renderizar tudo.

## Etapa 3 — Edit Decision Plan

Registrar o plano de edição usando `templates/edit-plan.example.yaml` como base.

O plano deve ser simples o suficiente para revisão humana e estruturado o suficiente para renderer ou agente executar.

## Etapa 4 — Edição

Executar o plano preferencialmente com FFmpeg e ferramentas auxiliares somente quando necessário.

Manter fonte bruta imutável.

## Etapa 5 — QC

Seguir `docs/QC.md`.

Avaliar o render final, não apenas roteiro ou timeline.

## Etapa 6 — Aprovação

Nenhuma peça é considerada pronta para saída externa antes da validação humana.

## Etapa 7 — Aprendizado

Registrar somente aprendizados de trabalho necessários para a próxima rodada:

- conceito testado;
- execução;
- versão;
- problema encontrado;
- correção aplicada;
- decisão de manter, revisar ou descartar.

Não transformar este repositório em arquivo de conversa ou contexto pessoal.

Usar `docs/LEARNING_LOOP.md` para registrar observações comparáveis. O aprendizado não pode depender de nomes soltos de arquivo, memória do operador ou prints sem contexto.