# AGENTS.md — Edição de Mídia O Segredo da Roça

## Missão

Transformar material real de imagem e vídeo do O Segredo da Roça em peças de mídia rastreáveis, úteis e revisáveis, sem inventar verdade comercial e sem executar ações externas automaticamente.

## Ordem obrigatória

1. Base: localizar e inventariar material, fatos e restrições.
2. Estrutura: definir conceito, hook, execução, formato e plano de edição.
3. Inteligência: só depois usar modelos para seleção, geração de variações, reframe, legendas ou QC.

## Regras

- Não publicar anúncios nem alterar campanhas, orçamento, público, pixel, evento, conta ou posicionamento.
- Não inventar claims, preço, prazo, promoção, garantia, prova social ou dado de performance.
- Não misturar dado ausente com zero ou fato confirmado.
- Preservar o material de origem; trabalhar por cópia, plano ou render versionado.
- Distinguir conceito de hook, execução, formato e variante.
- Não contar alteração cosmética como conceito novo sem justificativa material.
- Preferir componentes pequenos e substituíveis a clonar plataformas inteiras.
- Antes de incorporar código externo, verificar licença, maturidade, dependências e necessidade operacional.
- Nenhum token, credencial, `.env`, chave ou informação pessoal deve entrar no Git.
- Contexto pessoal permanece fora deste repositório.
- Toda saída para uso externo exige validação humana.

## Saída mínima para edição não trivial

Registrar:

- arquivos de origem;
- objetivo da peça;
- conceito;
- hook;
- execução;
- formato e duração;
- edit plan/timestamps;
- versão;
- resultado do QC;
- pendências humanas;
- hipótese e variável principal alterada;
- template editorial usado;
- observação de performance, quando disponível;
- decisão e justificativa.

- Não declarar uma variante vencedora sem janela, denominador, objetivo e observações comparáveis.
- Não confundir sinal de mídia com diagnóstico causal; registrar limites e mudanças concorrentes.
- Preservar observações históricas: corrigir por novo registro, não sobrescrever resultado anterior.
- Seguir `docs/PADRAO_EDICAO_OSDR.md`: gancho em 2 s, ritmo por template, legenda em blocos curtos, som de produto, fechamento sem despedida.

## Skill principal

Usar `.claude/skills/arquiteto-de-midia/SKILL.md` como control plane para inventário, arquitetura criativa, planos de edição, variantes e QC.

## Subagentes e skills de etapa

Seis subagentes em `.claude/agents/` (`preprocessador`, `diretor-criativo`, `refinador-de-corte`, `renderer`, `revisor-qc`, `guardiao-da-verdade`) e seis skills de etapa em `.claude/skills/` operam os scripts. O mapa completo está em `docs/MAQUINA_DE_EDICAO.md`. Nenhum agente aprova peça para mídia; cada um devolve saída versionada e pendências humanas.

## Escopo deste repositório

Este repositório carrega o método, a infraestrutura e a máquina de edição da bancada. O padrão editorial da casa está em `docs/PADRAO_EDICAO_OSDR.md` como referência versionada; instruções pessoais de operadores, fatos comerciais e contexto de clientes ficam fora daqui.
