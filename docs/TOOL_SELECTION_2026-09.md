# Seleção de ferramentas de edição — 2026-09-18

Escopo: edição para mídia paga com bruto real. Pesquisa em fontes primárias: metadados de repositórios, READMEs selecionados e licenças. Não é benchmark comparativo nem afirmação de melhores ferramentas universais. Data de push indica atividade, não prova qualidade ou segurança. Nenhum projeto inteiro foi clonado ou vendorizado.

## Decisão para a bancada

FFmpeg é o motor efetivamente usado e testado. faster-whisper ganhou adapter opcional local; PySceneDetect usa seu próprio CLI. Kdenlive/Shotcut são alternativas de acabamento humano. Não instalar a lista inteira.

| Fonte | Capacidade | Decisão / incorporação | Licença / limites | Dependências e risco | Último push consultado |
|---|---|---|---|---|---|
| [FFmpeg/FFmpeg](https://github.com/FFmpeg/FFmpeg) | Executar cortes, concatenação e pad | ADOPT: motor chamado via CLI; testado | LGPL/GPL conforme build; conferir configuração | Baixo; local; libx264 muda obrigações de distribuição | 2026-09-18 |
| [Breakthrough/PySceneDetect](https://github.com/Breakthrough/PySceneDetect) | Indexar cenas e exportar CSV | ADOPT opcional: CLI detect-content/list-scenes; não instalado | BSD-3-Clause | Médio; Python/OpenCV; sem GPU obrigatória | 2026-09-15 |
| [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) | Transcrição com timestamps de palavras | ADAPT: adapter local; teste simulado, sem inferência | MIT; pesos e dependências têm verificação própria | Médio; CTranslate2/PyAV; CPU INT8; modelos locais | 2025-11-19 |
| [KDE/kdenlive](https://github.com/KDE/kdenlive) | Acabamento humano multicamada | REFERENCE: editor externo, não embutido | GPL-3.0 identificada pelo GitHub | Baixo acoplamento; MLT/Qt; testar no computador do editor | 2026-09-18 |
| [mltframework/shotcut](https://github.com/mltframework/shotcut) | Acabamento humano alternativo | REFERENCE: alternativa ao Kdenlive, não instalar ambos sem necessidade | GPL-3.0 | Baixo acoplamento; MLT/Qt | 2026-09-17 |
| [mifi/lossless-cut](https://github.com/mifi/lossless-cut) | Seleção rápida sem recompressão | REFERENCE: ferramenta externa de rough cut | GPL-2.0 | Cortes lossless dependem de keyframes; conferir precisão | 2026-09-14 |
| [WyattBlue/auto-editor](https://github.com/WyattBlue/auto-editor) | Primeiro passe de silêncio | REFERENCE: rough cut supervisionado | Unlicense no código; binários têm outros componentes | Pode remover pausa expressiva; não é juiz criativo | 2026-09-13 |
| [OpenCut-app/OpenCut](https://github.com/OpenCut-app/OpenCut) | Editor web/API/MCP | REFERENCE: não adotar a reescrita como base estável | MIT | README informa reescrita; classic é separado | 2026-08-10 |
| [remotion-dev/remotion](https://github.com/remotion-dev/remotion) | Motion graphics React e vídeos parametrizados | REFERENCE: só adotar após licença e caso concreto | Licença própria, não MIT | Node/React; verificar elegibilidade comercial, equipe e versão | 2026-09-18 |
| [google-ai-edge/mediapipe](https://github.com/google-ai-edge/mediapipe) | Landmarks para apoio ao enquadramento | REFERENCE: não resolve sozinho o tracking de produto | Apache-2.0 no código | Modelos/tarefas têm termos próprios; testar crop | 2026-09-18 |
| [facebookresearch/sam2](https://github.com/facebookresearch/sam2) | Máscaras e tracking de objetos | REFERENCE: laboratório, não base obrigatória | Apache-2.0 identificado; verificar pesos | Alto custo relativo de GPU e integração | 2026-05-30 |
| [danielgatis/rembg](https://github.com/danielgatis/rembg) | Remoção de fundo estático | REFERENCE: apenas quando necessário | MIT no código; modelo separado | ONNX e pesos; risco de apagar partes do produto | 2026-09-08 |
| [poseljacob/agentic-video-editor](https://github.com/poseljacob/agentic-video-editor) | Separação director/refiner/reviewer | REFERENCE: padrão, sem importar agentes | MIT | Gemini/serviços externos; não enviar bruto sem decisão | 2026-04-14 |
| [bussiomedia-sys/forwrdcut](https://github.com/bussiomedia-sys/forwrdcut) | EDP, cache por segmento, QC e claims | HARVEST conceitual; sem copiar código | MIT confirmado no LICENSE; Inter OFL separado | CLI/MCP amplo; auditar cada módulo antes de adoção | 2026-07-15 |
| [gitethanwoo/video-editing](https://github.com/gitethanwoo/video-editing) | Análise editorial, B-roll, render e QC | REFERENCE: candidato novo para avaliação pontual | MIT informado no repo e README | Python/FFmpeg; extras Gemini/Remotion/MLX não são base | 2026-07-29 |

## Intercâmbio editorial

[AcademySoftwareFoundation/OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO): Apache-2.0, último push consultado 2026-09-18. Representa timelines; não renderiza vídeo. Decisão REFERENCE: considerar adapter quando houver troca real com editor/NLE. Verificar o formato suportado pelo editor antes de implementar. A consulta ao namespace OpenTimelineIO/OpenTimelineIO retornou 404; a organização correta foi verificada.

## Referências de implementação

- [SYSTRAN/faster-whisper @ ed9a06cd89a93e47838f564998a6c09b655d7f43](https://github.com/SYSTRAN/faster-whisper/tree/ed9a06cd89a93e47838f564998a6c09b655d7f43): snapshot consultado; não vendorizado.
- [Breakthrough/PySceneDetect @ 2fa8290de0353d371eaae92a8a6efb69d16a1e0c](https://github.com/Breakthrough/PySceneDetect/tree/2fa8290de0353d371eaae92a8a6efb69d16a1e0c): snapshot consultado; não vendorizado.
- [gitethanwoo/video-editing @ 166eed9b1f391af5201a37057924593bf8f413d4](https://github.com/gitethanwoo/video-editing/tree/166eed9b1f391af5201a37057924593bf8f413d4): snapshot consultado; não vendorizado.
- [bussiomedia-sys/forwrdcut @ 3f61f8c51896c830d81bf17fe009e39f0704bf97](https://github.com/bussiomedia-sys/forwrdcut/tree/3f61f8c51896c830d81bf17fe009e39f0704bf97): snapshot consultado; não vendorizado.

- [Filtros FFmpeg](https://ffmpeg.org/ffmpeg-filters.html): scale/pad/fps e concatenação; execução CLI restrita no renderer.
- [Licença FFmpeg](https://ffmpeg.org/legal.html): configuração do binário importa.
- [ForwrdCut LICENSE](https://github.com/bussiomedia-sys/forwrdcut/blob/main/LICENSE): a API classificava como Other, mas o arquivo contém MIT e nota separada da fonte Inter.
- [Remotion LICENSE](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md): licença de duas modalidades; não presumir gratuidade comercial com base no nome open source.

## Próxima adoção, condicionada a prova

1. Rodar transcrição PT-BR com um lote autorizado: conferir fala, nomes, preços, timestamps, RAM e tempo; comparar com a transcrição atual.
2. Rodar detecção de cenas no mesmo lote: medir se reduz busca manual sem perder demonstrações.
3. Se a demanda exigir legendas, música e multicamadas, experimentar Kdenlive como editor externo antes de criar essas funções.
4. Só depois avaliar extração de cache/QC do ForwrdCut e intercâmbio OTIO. Cada incorporação exige revisão do arquivo exato, dependências e atribuição.

## O que ainda falta para chamar de exemplar em produção

Teste de aceitação com mídia real e aprovação do editor; QC visual/áudio em celular; legenda e transcrição verificadas; comparação entre formatos; CI remoto verde; lock transitivo de dependências e revisão periódica de vulnerabilidades; decisão do titular sobre licença própria. O motor atual é um rough-cut seguro e limitado, não substituto de um editor completo.
