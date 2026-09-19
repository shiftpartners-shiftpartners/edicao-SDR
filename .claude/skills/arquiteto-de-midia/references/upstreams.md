# Upstreams recomendados

## Base
- FFmpeg/FFmpeg — motor de processamento e render. Licença principalmente LGPL, com partes opcionais GPL.
- Breakthrough/PySceneDetect — detecção de cenas; útil para indexação e seleção de trechos.
- openai/whisper — transcrição multilíngue e timestamps.
- WyattBlue/auto-editor — primeiro passe automático por silêncio/movimento; usar assistido.

## Apoio visual
- google-ai-edge/mediapipe — landmarks e visão leve para reframe/face tracking.
- facebookresearch/sam2 — segmentação/tracking de objetos; opção pesada.
- danielgatis/rembg — remoção de fundo; revisar também licença dos modelos usados.

## Interface humana
- mifi/lossless-cut — rough cut rápido e sem recompressão; GPL-2.0.
- OpenCut-app/OpenCut — editor open source; observar a reescrita atual e não acoplar a produção antes de estabilizar.

## Render programático
- remotion-dev/remotion — vídeo programático em React; licença especial, revisar antes de uso comercial.
- remotion-dev/skills — skills da organização para criação, rendering, captions e multimedia.

## Referências de arquitetura agêntica
- poseljacob/agentic-video-editor — arquitetura Director → Trim Refiner → Editor → Reviewer, com EditPlan versionado.
- bussiomedia-sys/forwrdcut — local-first, não destrutivo, reproduzível, FFmpeg por baixo, pesquisa/hooks/QC; MIT.

## Regra de incorporação

Não clonar um repositório inteiro só porque ele parece sofisticado. Preferir dependência, adapter, schema, padrão de pipeline, template ou pequena implementação compatível com a licença.