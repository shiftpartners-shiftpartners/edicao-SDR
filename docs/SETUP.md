# Instalação e primeiro uso

Python 3.11+ e FFmpeg/FFprobe com libx264 e AAC no PATH. Instale FFmpeg a partir de uma distribuição confiável; confira a licença do build. Não há GPU, conta de API ou serviço pago obrigatório.

    python -m venv .venv

Ative o ambiente: Linux/macOS `source .venv/bin/activate`; Windows PowerShell `.venv\Scripts\Activate.ps1`.

    python -m pip install -r requirements.txt
    ffmpeg -version
    ffprobe -version
    python -m unittest discover -s tests -v

Os testes de render usam material sintético. Se FFmpeg faltar, serão pulados: isso não constitui aprovação do render.

## Render de cortes sequenciais

O YAML antigo é planejamento editorial. O JSON `templates/render-plan.example.json` é o contrato executável v1; não são intercambiáveis. Preencha trechos válidos da sua mídia.

    python scripts/render_plan.py templates/render-plan.example.json --source-root media/source --out media/renders/teste-v01.mp4

Esse comando só valida e descreve. Para renderizar, acrescente `--execute`.

Suporta: cortes sequenciais, pad sem recortar produto, quatro proporções, 30 fps, H.264/AAC, áudio original ou silêncio quando ausente. Limites locais: 30 trechos e 180 segundos. Não são exigências da Meta.

Não suporta: transições, legenda queimada, trilha musical, auto-reframe, imagens estáticas ou edição multicamada. Use editor humano para acabamento. Campos desconhecidos são rejeitados.

O render gera um relatório lateral com hashes, plano, versão FFmpeg, duração e três verificações técnicas. Isso não aprova texto, áudio perceptual, direitos nem verdade comercial. Sempre verifique o resultado em celular.

Outputs existentes são recusados; escolha nova versão. Se houver relatório sem MP4 após uma falha de promoção, preserve para diagnóstico e tente com novo nome. A promoção usa hard links no mesmo filesystem; em filesystem sem suporte ela falha explicitamente.

## Do EDP ao render, QC e handoff

    python scripts/edp_to_render_plan.py media/work/peca.edit-plan.yaml --out media/work/peca.render-plan.json

Converte o YAML editorial no JSON v1. Instruções que o renderer não executa (crop, texto, transição, trilha, velocidade) fazem a conversão falhar; com `--unsupported report` elas são listadas para acabamento humano e o plano sai só com os cortes.

    python scripts/qc_render.py media/renders/peca__v01.mp4 --format 9:16 --max-seconds 15 --out media/renders/peca__v01.qc.json

Checa H.264/AAC, geometria do formato, fps 30, decode completo, abertura preta, áudio mudo e clipping. Veredito `pass` é "apto a testar"; criativo e verdade continuam humanos.

    python scripts/diversity_check.py media/work/ledger.jsonl --out media/work/diversidade-v01.md
    python scripts/handoff_pack.py media/work/ledger.jsonl <creative_id> --objective "..." --approved-by "..." --qc-report media/renders/peca__v01.qc.json

A auditoria reprova gêmeas cosméticas declaradas como diferença material. O handoff recusa `creative_id` sem `human_approval: approved` (use `--draft` para prévia). `make help` lista os atalhos.

## Legenda segmentada (padrão OSDR)

    python scripts/caption_segments.py media/work/transcript-v01.json --out media/work/legenda-v01.json --srt media/work/legenda-v01.srt

Quebra a fala em blocos de 3 a 5 palavras, aponta travessão e blocos longos demais, e gera SRT para importar no editor (CapCut, Kdenlive). Aceita `.txt` sem timestamps (sem SRT). Revisão humana obrigatória.

QC por template editorial: `python scripts/qc_render.py render.mp4 --template meta-ad` aplica formato e janela de duração de `templates/osdr-formats.json`.

## Transcrição opcional

Adapter: `scripts/transcribe_local.py`, integrado a faster-whisper por interface pública. Teste atual: contrato simulado, não qualidade de fala real. Não instalamos modelos nem executamos inferência nesta entrega.

Após aprovação e instalação de uma versão do faster-whisper compatível com seu ambiente e modelo multilíngue licenciado, já disponível localmente:

    python scripts/transcribe_local.py media/source/exemplo.mp4 --model-dir /caminho/modelo-local --out media/work/transcript-v01.json

CPU INT8; não faz download automático. Revisar nomes, preços e timestamps manualmente. Não usar um modelo somente inglês para português.

## Cenas opcionais

PySceneDetect disponibiliza seu próprio CLI; não é necessário recriá-lo. Instale somente se a duração/quantidade do material justificar. Interface documentada no upstream:

    scenedetect -i media/source/exemplo.mp4 detect-content list-scenes

Execute em diretório de trabalho fora do bruto e confira o CSV antes de escolher cortes. Esta integração é uma receita documentada, não foi instalada/testada nesta entrega.

## Limites de segurança

Mídia de terceiros pode explorar decoders. Processar somente arquivos autorizados, manter FFmpeg atualizado e usar ambiente isolado, sem credenciais e sem rede, para entradas não confiáveis. Os scripts não equivalem a uma sandbox.

Planos, transcrições e métricas reais ficam em `media/work/` (ignorado pelo Git). Só exemplos sintéticos entram no repositório. Não há licença open source concedida ao código próprio sem decisão do titular; licenças upstream não se propagam como autorização sobre este repositório.
