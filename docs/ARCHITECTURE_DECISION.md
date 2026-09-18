# Decisão técnica — 2026-09-18

Classificação: ARCHITECTURAL, implementação limitada à bancada local.

## Estado observado

Antes desta revisão o repositório tinha método (docs, templates) e dois utilitários (inventário e contact sheet), sem render, sem validação de registros, sem QC automático, sem agentes e sem CI. O repositório irmão FDR já tinha render limitado, validação estrita e testes.

## Opções

- Mínima: só copiar os scripts do FDR.
- Completa: integrar editor agêntico, transcrição real, tracking, frontend.
- Pragmática (escolhida): portar a base validada do FDR, acrescentar a camada OSDR (padrão editorial, templates por formato, legenda segmentada, QC por template) e operar por agentes e skills de etapa com gate humano.

## Contratos e limites

EDP YAML é editorial; render-plan JSON v1 é executável e rejeita campos desconhecidos. O bruto é somente leitura. Outputs existentes nunca são sobrescritos. Nada envia mídia a serviços, publica anúncios ou altera campanhas. Fatos comerciais (preço, prazo, rota, kit) não vivem neste repositório; vivem na fonte autorizada e entram por brief.

## Risco, prova e reversão

Risco principal: render tecnicamente válido e criativamente fraco. Mitigação: QC criativo humano/agente obrigatório e padrão editorial explícito. Testes usam mídia sintética; CI instala FFmpeg. Reverter o commit preserva mídia local.

## Fora do escopo

Autopublicação, GPU obrigatória, SaaS pago, download automático de modelos, ranking automático de criativos, promessa de performance.
