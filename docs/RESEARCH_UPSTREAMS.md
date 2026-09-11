# Pesquisa de componentes reutilizáveis — edição de mídia

Pesquisa inicial de projetos que podem contribuir para a bancada sem transformar o repositório em um clone de plataforma.

## Decisão arquitetural

**Não clonar tudo.** A preferência é incorporar somente o que resolver uma função clara: dependência, adapter, schema, padrão de pipeline, template ou pequena implementação compatível com licença e manutenção.

## 1. Base de processamento

### FFmpeg/FFmpeg
- Função: corte, concatenação, filtros, crop/scale, áudio, legendas, codec e render.
- Papel aqui: motor-base.
- Observação: configuração de build e licença importam.

### Breakthrough/PySceneDetect
- Função: detectar cortes e transições, dividir vídeo e salvar frames representativos.
- Papel aqui: indexação de cenas antes da seleção por agente/humano.

### openai/whisper
- Função: reconhecimento de fala multilíngue, tradução e identificação de idioma.
- Papel aqui: transcrição e timestamps para busca, legendagem e seleção de trechos falados.

### WyattBlue/auto-editor
- Função: primeiro passe automático por volume/silêncio e outros métodos; export de sequências/timelines.
- Papel aqui: rough cut assistido, nunca juiz criativo final.

## 2. Visão e manipulação

### google-ai-edge/mediapipe
- Função: visão leve, landmarks e tracking.
- Papel possível: apoio a auto-reframe e enquadramento de rosto/corpo.
- Decisão: opcional; só incluir quando houver caso real.

### facebookresearch/sam2
- Função: segmentação e tracking de objetos em imagem/vídeo.
- Papel possível: isolamento de produto, máscara e efeitos seletivos.
- Decisão: opcional pesado; não trazer para a base mínima.

### danielgatis/rembg
- Função: remoção de fundo.
- Papel possível: tratamento de assets estáticos.
- Decisão: opcional; verificar licença do modelo selecionado.

## 3. Referências de arquitetura agêntica

### poseljacob/agentic-video-editor
- Arquitetura de interesse: `Preprocess → Director → Trim Refiner → Editor → Reviewer`.
- O que interessa: schema e separação de papéis, não necessariamente clonar toda a aplicação.

### bussiomedia-sys/forwrdcut
- Recursos de interesse: pesquisa de shots, hooks, reframe, captions, templates e QC.
- Decisão: referência forte para estudo e reaproveitamento parcial do cérebro/fluxo.

## 4. Editores e render programático

### mifi/lossless-cut
- Uso: ferramenta humana auxiliar para triagem/corte sem recompressão.
- Decisão: usar externamente; não copiar código sem necessidade.

### OpenCut-app/OpenCut
- Papel possível: editor open source com potencial de integração futura.
- Decisão: observar e avaliar somente quando houver necessidade real.

### remotion-dev/remotion + remotion-dev/skills
- Função: vídeo programático, rendering e organização modular de captions/metadata.
- Decisão: referência forte; avaliar licença aplicável antes de adoção comercial.

## 5. Meta / Andromeda

A fonte pública primária usada aqui é a publicação de engenharia da Meta sobre Andromeda. Ela descreve um sistema proprietário de ML para **ads retrieval**, voltado a um universo de criativos muito maior, personalização e eficiência.

Isso sustenta a necessidade de uma produção capaz de criar e organizar diversidade criativa de forma material. Não sustenta regras inventadas como “Andromeda exige exatamente N conceitos”.

Fonte: https://engineering.fb.com/2024/12/02/production-engineering/meta-andromeda-advantage-automation-next-gen-personalized-ads-retrieval-engine/

## Conclusão

Para o estágio atual, a composição mais enxuta é:

**FFmpeg + inventário + contact sheets + Whisper quando necessário + EDP + revisão humana**.

PySceneDetect e auto-editor entram quando o material justificar. ForwrdCut e agentic-video-editor funcionam como fontes de arquitetura. SAM 2, MediaPipe, rembg, Remotion e OpenCut entram somente por demanda real.
