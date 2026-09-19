# Como usar — bancada de edição O Segredo da Roça

Guia curto para operar sem entender a arquitetura inteira.

## O que isto faz

Pega material bruto (vídeo e foto da panela, da comida, da rota), organiza o que existe, define conceitos diferentes de verdade, prepara cortes, legenda e variantes, revisa tudo e só então libera para a Ágatha subir em mídia.

**material bruto → inventário → conceito → plano de edição → render → QC → aprovação humana → handoff**

Nada aqui publica anúncio, altera campanha ou inventa preço.

## Onde colocar os arquivos

```text
media/source/        # originais, nunca alterados, fora do Git
media/work/          # índices, planos, legendas, ledger
media/contact-sheets/
media/renders/
```

## Passo a passo com o Claude Code

Peça em linguagem natural; cada pedido aciona uma skill de etapa.

1. **"Inventaria esses vídeos."** → `inventariar-material`. Sai índice técnico + pranchas de frames.
2. **"Monta 3 conceitos diferentes para anúncio Meta de 6 a 9 s."** → `planejar-edicao`. Sai matriz + EDP por variante, com pendências.
3. **"Renderiza a C01."** → `renderizar-corte`. Sai MP4 versionado + relatório; legenda segmentada quando há fala.
4. **"Faz o QC."** → `qc-render`. Sai veredito técnico por template + parecer criativo + conferência de verdade comercial.
5. **"São variantes de verdade?"** → `auditar-diversidade`.
6. **"Fecha o handoff da C01."** → `handoff-midia`. Só sai com aprovação humana registrada.

## Passo a passo no terminal

```bash
make setup                         # instala dependências e confere FFmpeg
make check                         # testes e validações
make inventory                     # índice de media/source
make sheet SRC=media/source/x.mp4  # prancha de frames
make plan ID=peca                  # EDP YAML → plano de render
make dry-run ID=peca               # valida sem renderizar
make render ID=peca                # renderiza (nunca sobrescreve)
make captions ID=peca              # legenda 3–5 palavras + SRT
make qc ID=peca TEMPLATE=meta-ad   # QC técnico por template OSDR
make diversity LEDGER=media/work/ledger.jsonl
make handoff ID=<creative_id> OBJ="conversas qualificadas" BY="nome/papel"
```

Templates disponíveis: `reel15`, `reel30`, `tiktok`, `meta-ad`, `meta-ad-feed`, `nano`, `story` (`templates/osdr-formats.json`).

## O que o renderer faz e não faz

Faz: cortes sequenciais, enquadramento com pad, 9:16 / 4:5 / 1:1 / 16:9, 30 fps, H.264/AAC, relatório com hash.
Não faz: legenda queimada, trilha, transição, reframe automático, multicamada. Isso é acabamento humano (CapCut, Kdenlive) a partir do SRT e do plano.

## Regra que não muda

Render pronto não é peça aprovada. Preço, prazo, rota, kit e brinde só entram com fonte autorizada. Aprovação é humana e fica registrada no ledger.
