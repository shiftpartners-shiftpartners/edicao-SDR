---
name: inventariar-material
description: Inventário técnico e visual de um lote de mídia bruta (footage-index + contact sheets) antes de qualquer decisão de corte. Use ao receber vídeos/imagens novos ou quando alguém pedir "o que temos de material".
---

# Inventariar material

1. Confirme que os arquivos estão em `media/source/` (fora do Git) e que nada será alterado lá.
2. Rode o índice, versionando a saída:
   ```bash
   python scripts/media_probe.py media/source --out media/work/footage-index-v01.json --hash
   ```
3. Gere uma prancha por vídeo candidato:
   ```bash
   python scripts/contact_sheet.py media/source/<video>.mp4 --out media/contact-sheets/<video>.png --frames 16
   ```
4. Leia as pranchas e classifique cenas por papel: hook, demonstração, prova, contexto, CTA. Timestamps ficam `a confirmar` até revisão no player.
5. Registre erros de mídia e pendências humanas.

Delegue ao agente `preprocessador` quando o lote tiver mais de cinco arquivos. Se FFmpeg faltar, registre bloqueio técnico com comando e erro; não invente inventário.
