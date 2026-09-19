# Missão: biblioteca inventariada do Drive · O Segredo da Roça (Kit Cozinha primeiro)

Para quem: um agente com acesso local ao Drive (Codex CLI na máquina da operação com Google Drive para desktop, ou Claude Code local). A bancada remota não consegue baixar arquivos do Drive acima de ~6 MB (bloqueio registrado em 18/09), por isso esta etapa roda fora dela.
Repositório de destino: `edicao-SDR` (branch de trabalho). Depois de OSDR, repetir em `edi-ofdr` com a lista de cenas do FDR.
Regra número 1: não alterar, mover, renomear nem apagar nada no Drive. Só ler e produzir índice, pranchas e relatório.
Regra número 2: nada de dado pessoal no índice (sem nome de cliente, telefone, endereço, rosto marcado como identificável fica só como "rosto: sim/não").

## 1. Entrada

- Pasta raiz do Drive: `Kit Cozinha` (nome exato a confirmar pela operação) e, se existirem, as irmãs `Kit Cozinha da Roça`, `Prontos`, `Depoimentos`, `Entregas`, `Panela cliente`.
- Extensões: .mp4 .mov .m4v .webm .jpg .jpeg .png .heic .webp
- Ignorar: arquivos abaixo de 200 KB, capturas de tela de conversa, PDFs, planilhas.

## 2. Ferramentas do repositório (não reinventar)

```bash
make setup                                   # dependências (FFmpeg, PyAV, Pillow)
python scripts/media_probe.py <pasta_drive> --out media/work/biblioteca/footage-index-osdr-v01.json --hash
python scripts/contact_sheet.py <video> --out media/contact-sheets/<nome>.png --frames 16
```
O índice sai no formato `{version, generated_at, source_dir, file_count, files[], errors[]}`; cada `files[]` tem `path, extension, size_bytes, duration_seconds, video{codec,width,height,orientation,fps}, audio{codec,sample_rate,channels}` e `sha256` com `--hash`.

## 3. O que buscar (lista de compras, não é ir cego)

Cada arquivo recebe uma ou mais etiquetas de cena. Só etiquetar o que se vê na prancha ou no player; sem suposição.

| Etiqueta | O que é | Serve para | Prioridade |
|---|---|---|---|
| `hook_fogo` | Panela na chama azul do gás ou fogo de lenha, close, primeiros 2 s limpos | T3 "Vai rachar?", T2 abertura | alta |
| `comida_borbulhando` | Moqueca, feijão, carne fervendo na panela de barro, colher de pau | T2 "Comida que abre o apetite" | alta |
| `mesa_servida` | Mesa com panelas de barro servidas, sem rosto | T2 fechamento, carrossel card 1 | alta |
| `kit_exposto_1080` | Kit completo arrumado, 1080p ou mais, fundo limpo | card do kit, CTA de todo corte | alta |
| `peca_isolada` | Uma peça só em uso (caldeirão, moquequeira, panela 5 L, panela 3 L, travessa, pimenteira, colher, tigela) | T5 "peça por peça", cards | alta |
| `entrega_real` | Entrega na porta, caixa aberta, cliente conferindo (rosto sim/não) | T1 "Confere antes de pagar", T6 | alta |
| `caminhao_rota` | Caminhão/van de entrega, placa de cidade, estrada, carregamento | T4 "O caminhão chega na sua cidade" | alta |
| `cura_panela` | Processo de cura, panela nova vs curada, tampa | T3 prova | média |
| `forno_lenha` | Panela no forno ou fogão a lenha | T3 prova "vai na lenha" | média |
| `lavar_guardar` | Lavagem, secagem, armazenamento | T3 "receber, lavar, cozinhar" | média |
| `depoimento_audio` | Cliente falando (áudio ou vídeo) sobre a panela | prova social, só com autorização | média |
| `presente` | Panela sendo dada de presente, embrulho, reação | T6 "Presente para quem cozinha" | média |
| `bastidor_producao` | Oleiro, barro, forno de produção, artesão | marca, confiança | baixa |
| `texto_preco_antigo` | Qualquer tela com "49,90", "frete grátis", "BIO", preço ou promessa antiga | BLOQUEIO: não reutilizar sem corte | marcar sempre |
| `rosto_identificavel` | Rosto de cliente reconhecível | exige autorização registrada | marcar sempre |
| `ia_gerada` | Imagem ou vídeo claramente gerado por IA | não substitui prova real em T1, T4, T6 | marcar sempre |

Para cada cena encontrada anotar: `arquivo, in, out (segundos), etiqueta, qualidade (1080p+/720p/abaixo), som de produto (sim/não), rosto (sim/não), texto na tela (transcrever), observação curta`.

## 4. Saída obrigatória (arquivos novos, nada sobrescrito)

1. `media/work/biblioteca/footage-index-osdr-v01.json` (media_probe, com hash).
2. `media/contact-sheets/osdr/<nome>.png` para todo vídeo com mais de 3 s.
3. `media/work/biblioteca/BIBLIOTECA_OSDR_v01.csv` com colunas: `arquivo,pasta_drive,duracao_s,resolucao,orientacao,in_s,out_s,etiqueta,qualidade,som_produto,rosto,texto_tela,observacao`.
4. `media/work/biblioteca/BIBLIOTECA_OSDR_v01.md`: resumo por etiqueta (quantas cenas, melhores 3 por etiqueta com arquivo e faixa), tabela "tem / falta" por conceito T1 a T6, lista de bloqueios (preço antigo, rosto, IA), erros de mídia (arquivos corrompidos, HEIC sem conversão).
5. Uma linha em `media/work/lote-t1t6/LOG.md` com data/hora BRT, pasta lida, contagem de arquivos, contagem por etiqueta.

## 5. Critério de pronto

- Todo arquivo da pasta aparece no índice ou na lista de erros.
- Toda cena de prioridade alta tem pelo menos "tem" ou "falta" declarado por conceito.
- Nenhum arquivo do Drive foi modificado (conferir por data de modificação antes e depois).
- CSV abre sem erro; MD sem travessão; sem dado pessoal.

## 6. Depois desta missão (fica com a bancada remota)

A bancada lê `BIBLIOTECA_OSDR_v01.csv`, monta EDPs só com faixas etiquetadas, renderiza pela esteira e entrega rascunhos para aprovação. A operação não volta a procurar cena nenhuma.

## 7. Prompt pronto para colar no Codex (ou em outro agente)

```
Você vai inventariar material de vídeo e imagem para uma bancada de edição. Leia primeiro docs/missoes/MISSAO_INVENTARIO_DRIVE_OSDR.md neste repositório e siga à risca. Pasta de entrada: <caminho local da pasta do Drive "Kit Cozinha">. Nunca altere, mova ou apague arquivos da pasta de entrada. Use os scripts do repositório (scripts/media_probe.py e scripts/contact_sheet.py) e produza exatamente as cinco saídas da seção 4, com os nomes indicados. Etiquete cenas só pelo que se vê nas pranchas ou no player, com as etiquetas da seção 3; marque sempre texto_preco_antigo, rosto_identificavel e ia_gerada quando aparecerem. Não escreva nome de cliente, telefone ou endereço em nenhum arquivo. Ao terminar, rode `make check` e me devolva: contagem de arquivos lidos, contagem por etiqueta, a tabela tem/falta por conceito e a lista de erros.
```
