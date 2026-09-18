# Meta Andromeda — tradução operacional segura

Fonte primária: Meta Engineering, “Meta Andromeda: Supercharging Advantage+ automation with the next-gen personalized ads retrieval engine”, 2 dez. 2024.

Andromeda é descrito pela Meta como um sistema proprietário de machine learning para retrieval em recomendação de anúncios. A publicação enfatiza escala muito maior do universo de criativos, personalização e eficiência do estágio de recuperação.

## Implicação operacional

Usar diversidade criativa material e rastreável. Não alegar que a Meta exige um número fixo de conceitos, hooks ou formatos se isso não estiver documentado em fonte primária.

Distinguir:
- conceito: tese/ideia central;
- hook: abertura que captura atenção;
- execução: forma concreta de materializar o conceito;
- formato: 9:16, 1:1, 4:5 etc.;
- variante: combinação versionada desses elementos.

## Atualização 2026-09

Em 2025 a Meta publicou o GEM (Generative Ads Model), modelo-base de recomendação de anúncios com sinais multimodais. Consequência segura: ampliar a rastreabilidade do criativo e do resultado; não tentar simular a decisão interna da plataforma.

Uma peça só entra no ciclo de aprendizagem quando tem: identidade estável (`creative_id`) e origem rastreável; conceito, hook, execução, formato e versão explícitos; hipótese e variável principal; QC técnico, criativo e de verdade aprovado; destino e objetivo registrados no handoff; observação posterior com janela e denominadores; decisão humana (`escalar`, `iterar`, `pausar`, `inconclusivo`).

Fontes: https://engineering.fb.com/2024/12/02/production-engineering/meta-andromeda-advantage-automation-next-gen-personalized-ads-retrieval-engine/ e https://engineering.fb.com/2025/11/10/ml-applications/metas-generative-ads-model-gem-the-central-brain-accelerating-ads-recommendation-ai-innovation/

