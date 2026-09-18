---
name: qc-render
description: QC técnico automático + revisão criativa e de verdade de um render antes da aprovação humana. Use quando pedirem "revisa", "faz o QC", "pode entregar?".
---

# QC do render

1. Técnico automático:
   ```bash
   python scripts/qc_render.py media/renders/<id>__v01.mp4 --template meta-ad --out media/renders/<id>__v01.qc.json
   ```
   Reprova: codec fora de H.264/AAC, geometria errada, abertura preta, áudio mudo ou decode com erro. Aviso: fps fora de 30, pico perto de 0 dB.
2. Visual: `python scripts/contact_sheet.py media/renders/<id>__v01.mp4 --out media/contact-sheets/<id>__v01.png`.
3. Criativo e distinção: agente `revisor-qc` com `docs/QC.md` e `docs/PADRAO_EDICAO_OSDR.md` (gancho 2 s, ritmo, legenda, som de produto, fechamento).
4. Verdade: agente `guardiao-da-verdade`.
5. Atualize o ledger: `status: qc_pending` → `approved` só após aprovação humana registrada (`human_approval: approved`), e valide com `scripts/validate_records.py`.

Veredito técnico `pass` significa "apto a testar", nunca "aprovado".
