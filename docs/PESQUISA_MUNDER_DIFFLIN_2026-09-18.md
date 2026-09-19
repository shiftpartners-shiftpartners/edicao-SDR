# Pesquisa: Munder Difflin (avaliação para a operação)

Data: 18/09/2026, 22:45 BRT. Pedido da operação: "procura esse repositório, veja o que ele tem de importante para a gente, o que utilizaríamos, o que não".
Fontes bloqueadas pelo proxy desta sessão: munderdiffl.in (site e blog), Product Hunt, Hacker News (e espelho hn.algolia), reviews de terceiros, api.github.com. O que entrou foi via github.com, raw.githubusercontent.com e snippets de busca. Onde só houve snippet, está marcado "snippet, não verificado na fonte".

## 1. O que é, em 5 linhas

Munder Difflin é um app desktop (Electron) open source que roda no computador do usuário e embrulha CLIs de agentes de código já instalados (Claude Code, Codex, Gemini CLI, Grok, Qwen, Copilot CLI, Cursor) como processos reais em terminais virtuais.
Um agente orquestrador chamado "Michael" recebe o briefing, distribui trabalho a outros agentes, roteia mensagens e escala para o humano só gastos, mudanças de escopo e operações destrutivas.
Os agentes coordenam por um "hive": repositório git local com memória em markdown por agente, caixas de mensagens em arquivo, quadro compartilhado e log de eventos.
Usa a assinatura que a pessoa já paga (limites por hora do plano) ou chaves de API próprias e modelos locais.
Foco visível é engenharia de software; a interface é uma paródia do seriado The Office, com avatares num escritório 2D.

## 2. Fatos verificados

| Item | Valor | Fonte |
|---|---|---|
| Repositório | https://github.com/chaitanyagiri/munder-difflin | GitHub API (MCP search_repositories) |
| Autor | chaitanyagiri (pessoa física) | GitHub API |
| Licença | MIT (código). Pixel art LimeZu com licença própria que exige atribuição | GitHub API; README |
| Estrelas | 7.612 (996 forks) | GitHub API, 19/09/2026 |
| Issues abertas | 93 issues (188 no contador da API, que inclui PRs) | página de issues do repo |
| Criado em | 31/05/2026 | GitHub API |
| Último push | 17/09/2026 (merge do PR #555) | página de commits |
| Linguagem | TypeScript (Electron, React, Pixi.js, xterm.js, node-pty) | GitHub API; README |
| Última release | v0.5.2 em 09/09/2026 (mac, Windows, Linux). README ainda diz "v0.4.6 pre-release" | página de releases; README |
| Instalação | Binário pronto ou fonte: Node 18+, npm, toolchain C/C++ (node-pty), pelo menos um CLI de agente no PATH | README |
| Como aciona os modelos | CLIs locais em pseudo-terminal, "com sua assinatura existente e seus limites por hora"; chaves por provedor num "secret broker"; Ollama/LM Studio/vLLM | README |
| Orquestração | "Michael é seu clone e o único agente que você brifa. Ele atribui o trabalho, roteia o tráfego e escala as poucas coisas que precisam de você" | README |
| Coordenação | Hive = repo git local: memória por agente, mailboxes em arquivo, blackboard, log append-only, "single-committer git" | README; docs/ARCHITECTURE.md; docs/message-queue.md |
| Divisão de tarefas | Kanban com dependências; Michael adjudica e atribui | docs/ARCHITECTURE.md |
| Merge | Worktrees git por agente (opcional). Procedimento de integração não documentado | README; docs/ARCHITECTURE.md |
| Revisão entre agentes | Não há papel de revisor documentado. Existem gates humanos (gasto, escopo, destrutivo), circuit breaker (orientar, restringir, parar) e "Ask Me" | README |
| Custo em tokens | Orçamento de tokens por agente, custo real lido dos transcripts, ledger. Sem números no README | README |
| Custo (relato do autor) | "Roda num plano Claude de US$ 100/mês com um orquestrador Opus e nove workers Sonnet, semanas sem bater limite" | snippet do blog, não verificado na fonte |
| SO | macOS, Windows, Linux | README |
| Integrações | Slack e webhooks. Telegram "em breve". Sem WhatsApp | README |
| Telemetria | Eventos anônimos; opt-out por Settings ou DO_NOT_TRACK | README |
| Repercussão | Post no HN com 303 pontos e 138 comentários, discussão dividida | snippets, não verificados |

Issues abertas relevantes (página de issues do repo):

| Issue | Tema |
|---|---|
| #301 (aberta pelo autor, 24/08) | Agentes fazem grep na máquina inteira e leem dados de outros apps, sem limite de escopo. Frase da issue: "um diálogo de permissão que dispara o tempo todo não é controle de segurança, é uma fila que o usuário aprende a limpar sem ler" |
| #441 (04/09) | Circuit breaker derruba agente que está trabalhando |
| #297 (24/08) | Saída do PTY apaga worktree do agente e descarta trabalho não integrado |
| #167 (17/08) | Pedido de acesso por navegador. Aberta, sem resposta do mantenedor |
| #163 (17/08) | "Proper MCP support" (aberta) |
| #535 (16/09) | Agentes não-Claude registram zero tokens/custo |
| #549 (17/09) | Windows: hooks do Claude Code falham com espaço no caminho |

## 3. O que serve para esta operação (inferência)

A ideia central já é a nossa: um orquestrador que brifa, delega e só escala ao humano gasto, escopo e ações destrutivas. Isso valida o desenho guardiao-da-verdade + aprovação humana no ledger.

Três mecanismos valem como referência de desenho, não como software a instalar:
- Memória por agente em markdown, versionada em git, com log append-only.
- Orçamento de tokens por agente com ledger de custo.
- Circuit breaker em escada (orientar, restringir, parar) para agente em loop.

## 4. O que não serve ou é risco

- Fato: é app desktop. Precisa de máquina ligada com os CLIs instalados. A operação roda pelo Claude Code na web, sem máquina dedicada. Acesso por navegador (#167) está aberto sem resposta.
- Fato: agentes rodam na assinatura local e seus limites por hora. Vários em paralelo consomem o mesmo plano. O relato de "9 workers sem bater limite" não foi verificado. #535 mostra medidor de custo falhando.
- Fato: segurança de credenciais é ponto fraco reconhecido pelo autor (#301). Numa máquina com tokens de Meta Ads, Drive, Railway e o bot do WhatsApp, é risco direto de vazamento.
- Fato: não há revisão entre agentes documentada. Não resolve "agente que fala qualquer coisa"; só freia gasto e loop.
- Fato: maturidade baixa. 3,5 meses, README em "pre-release", 93 issues abertas, bugs que descartam trabalho (#297).
- Fato: foco é código. Sem WhatsApp. Sem MCP "de verdade" (#163), então Meta Ads, Drive e Railway não entram.
- Inferência: instalar Node, toolchain C/C++ e manter um Electron rodando é custo de manutenção que hoje não existe.

## 5. O que já temos que cobre a mesma necessidade

- Claude Code remoto com sessões filhas, mensagens entre sessões e Routines agendadas: é o "escritório de agentes" sem máquina local.
- Subagentes em `.claude/agents/` e skills de etapa em `.claude/skills/` nos dois repositórios, mais `guardiao-da-verdade` e `human_approval: approved` no ledger.
- MCPs de Meta Ads, Drive, Railway e GitHub conectados na sessão remota, coisa que o Munder não oferece.
- Memória e handoff via `cabecalho-de-retomada` e `atualizacao-da-fonte-mae`.

O que falta aqui e o Munder faz: orçamento de tokens por agente com ledger e freio automático de loop. Ambos podem virar regra de skill e coluna no ledger, sem instalar nada.

## 6. Veredito

Ignorar como ferramenta (exige máquina local, é focado em código, expõe credenciais e não tem revisão entre agentes). Aproveitar só como referência de desenho para memória por agente, orçamento por agente e freio de loop.

## 7. Se for testar depois (3 passos mínimos)

Só se houver máquina dedicada ou a issue #167 fechar com acesso por navegador:
1. Instalar o binário numa máquina limpa, sem nenhum token de Meta Ads, Drive, Railway ou WhatsApp, só com Claude Code logado num plano separado.
2. Rodar um único fluxo de baixo risco (inventário de material) com 1 orquestrador e 2 workers e medir consumo do plano por hora frente ao mesmo fluxo como subagente no Claude Code remoto.
3. Verificar se #301, #163 e #297 foram fechadas antes de qualquer uso com dados reais.
