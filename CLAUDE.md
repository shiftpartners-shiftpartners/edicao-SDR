# CLAUDE.md — Edição de Mídia O Segredo da Roça

Leia `AGENTS.md`, `.claude/skills/arquiteto-de-midia/SKILL.md` e `docs/PADRAO_EDICAO_OSDR.md` antes de executar qualquer tarefa de edição ou planejamento criativo neste repositório. O mapa etapa × script × agente × skill está em `docs/MAQUINA_DE_EDICAO.md`.

Prioridades:

1. Reaproveitar material real antes de gerar material novo.
2. Organizar o raciocínio de mídia antes de renderizar.
3. Produzir variações materialmente diferentes, não apenas cosméticas (`scripts/diversity_check.py`).
4. Trabalhar de forma não destrutiva e versionada: nunca sobrescrever render, índice ou relatório.
5. Manter aprovação humana antes de qualquer saída para campanha (`human_approval: approved` no ledger).

Skills de etapa em `.claude/skills/`: `inventariar-material`, `planejar-edicao`, `renderizar-corte`, `qc-render`, `auditar-diversidade`, `handoff-midia`. Subagentes em `.claude/agents/`. Rode `make check` antes de dizer que algo funciona.

Quando houver dúvida entre construir do zero e reaproveitar open source, leia `docs/TOOL_SELECTION_2026-09.md` e `docs/RESEARCH_UPSTREAMS.md` e prefira o menor componente que resolva a necessidade.

Fatos comerciais (preço, prazo, frete, rota, kit, brinde, garantia, prova social) não vivem aqui: entram por brief com fonte autorizada e passam pelo agente `guardiao-da-verdade`.

Não publicar, não alterar mídia bruta, não expor credenciais e não registrar informações pessoais.
