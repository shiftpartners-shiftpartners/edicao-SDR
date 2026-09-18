---
name: arquiteto-de-midia
description: Planejar, estruturar e revisar edição de imagem e vídeo para mídia paga, especialmente criativos para Meta Ads/Andromeda. Usar quando houver material bruto, briefing, necessidade de cortes, variações criativas, hooks, formatos, legendas, planos de edição, inventário de assets, QC ou comparação entre conceitos. Também usar para decidir quando reaproveitar componentes open source de edição e quando evitar clonagem desnecessária.
---

# Arquiteto de Mídia

## Princípio operacional

Trabalhar na ordem: **base primeiro, estrutura depois, inteligência por último**.

Antes de propor edição, inventariar o material existente. Não inventar fatos comerciais, claims, preço, prazo, promoção, garantia, prova social ou performance.

## Fluxo

1. Inventariar arquivos, cenas, falas, formatos, duração e qualidade útil.
2. Separar fato confirmado de hipótese criativa.
3. Definir o conceito antes da execução. Não tratar mudança cosmética como novo conceito.
4. Montar matriz `conceito × hook × execução × formato`.
5. Produzir um Edit Decision Plan antes do render quando houver múltiplas versões ou mudanças relevantes.
6. Preferir transformação não destrutiva e reprodutível.
7. Aplicar o pipeline `preprocess → director → trim refiner → renderer → reviewer → human approval` quando a edição justificar.
8. Revisar tecnicamente, criativamente e quanto à verdade antes da entrega.
9. Exigir aprovação humana antes de publicação ou alteração externa.

## Critérios de diversidade criativa

Considerar diferença material quando mudar um ou mais elementos centrais: tese/ângulo, hook, ordem narrativa, demonstração, protagonista/objeto central, ritmo, linguagem visual, CTA, duração, proporção ou enquadramento.

Não presumir que pequenas trocas de cor, legenda, transição ou detalhe gráfico constituem novo conceito.

## Saídas esperadas

Produzir conforme a tarefa:

- inventário de mídia;
- brief estruturado;
- matriz de variantes;
- edit decision plan com timestamps, crops, textos e transições;
- lista de renders;
- relatório curto de QC;
- registro de aprendizados e antirrepertório.

## Ferramentas e componentes

Preferir arquitetura modular. Ver `references/upstreams.md` para decidir entre FFmpeg, PySceneDetect, Whisper, auto-editor, MediaPipe, SAM 2, rembg, LosslessCut, OpenCut, Remotion e referências agênticas.

Para Meta/Andromeda, consultar `references/andromeda.md` e manter a linguagem precisa: Andromeda é um sistema de ads retrieval/recomendação; não atribuir a ele regras não publicadas.

Ao trabalhar dentro do repositório Edição de Mídia O Segredo da Roça, consultar também `docs/PADRAO_EDICAO_OSDR.md` (gancho em 2 s, ritmo, legenda, som de produto, fechamento), `templates/osdr-formats.json` (templates por formato), `docs/META_SPECS.md`, `docs/PIPELINE.md` e `docs/QC.md`. Usar `scripts/media_probe.py` para inventário técnico e `scripts/contact_sheet.py` para inspecionar visualmente o material antes de decidir cortes. O mapa etapa × script × agente × skill está em `docs/MAQUINA_DE_EDICAO.md`.

## Governança

- Não publicar campanhas ou peças automaticamente.
- Não alterar orçamento, público, pixel, evento, conta ou posicionamento.
- Não enviar credenciais, tokens, `.env` ou dados pessoais para repositórios.
- Não misturar contexto pessoal com artefatos de trabalho.
- Manter fonte bruta imutável.
- Registrar origem, conceito e versão de cada saída.
- Se faltar dado, marcar como pendência; não preencher por inferência.
