# Bancada de edição — atalhos locais. Nenhum alvo publica, altera campanha ou toca em media/source/.
PY ?= python
ID ?= exemplo
TEMPLATE ?= meta-ad

.PHONY: setup check test validate diversity inventory sheet normalize plan dry-run render finish qc captions handoff lote help

help:
	@echo "make setup | check | inventory | sheet SRC=... | normalize SRC=... | plan ID=... | dry-run ID=... | render ID=... | finish ID=... VO=... | qc ID=... | diversity | handoff ID=... OBJ=... BY=... | lote LOTE=media/work/<lote>"

setup:
	$(PY) -m pip install -r requirements.txt
	ffmpeg -version | head -1
	ffprobe -version | head -1

test:
	$(PY) -m unittest discover -s tests -v

validate:
	$(PY) scripts/validate_records.py templates/creative-ledger.example.jsonl --schema schemas/creative-variant.schema.json
	$(PY) scripts/validate_records.py templates/performance-observations.example.jsonl --schema schemas/performance-observation.schema.json

diversity:
	$(PY) scripts/diversity_check.py $(or $(LEDGER),templates/creative-ledger.example.jsonl)

check: test validate diversity

inventory:
	$(PY) scripts/media_probe.py media/source --out media/work/footage-index-$(shell date +%Y%m%d-%H%M%S).json --hash

sheet:
	$(PY) scripts/contact_sheet.py $(SRC) --out media/contact-sheets/$(notdir $(basename $(SRC))).png --frames 16

normalize:
	$(PY) scripts/normalize_source.py $(SRC)

plan:
	$(PY) scripts/edp_to_render_plan.py media/work/$(ID).edit-plan.yaml --out media/work/$(ID).render-plan.json --unsupported report

dry-run:
	$(PY) scripts/render_plan.py media/work/$(ID).render-plan.json --source-root media/source --out media/renders/$(ID).mp4

render:
	$(PY) scripts/render_plan.py media/work/$(ID).render-plan.json --source-root media/source --out media/renders/$(ID).mp4 --execute

finish:
	$(PY) scripts/finish_draft.py media/work/$(ID).edit-plan.yaml media/renders/$(ID).mp4 --out media/renders/$(ID)-draft.mp4 $(if $(VO),--vo $(VO),)

qc:
	$(PY) scripts/qc_render.py media/renders/$(ID).mp4 --template $(TEMPLATE) --out media/renders/$(ID).qc.json

captions:
	$(PY) scripts/caption_segments.py media/work/$(ID).transcript.json --out media/work/$(ID).legenda.json --srt media/work/$(ID).legenda.srt

lote:
	$(PY) scripts/lote_run.py $(LOTE)

handoff:
	$(PY) scripts/handoff_pack.py media/work/ledger.jsonl $(ID) --objective "$(OBJ)" --approved-by "$(BY)" --qc-report media/renders/$(ID).qc.json --out media/work/handoff-$(ID).md
