# Build: latexmk + pdfLaTeX, with Beamer and Metropolis installed.
# Optional figure editing: draw.io Desktop; Python packages in requirements.txt.
TEX = main.tex
OUT = build
PYTHON ?= python3
DRAWIO ?= drawio
DIAGRAMS = $(wildcard figures/diagrams/*.drawio)

.PHONY: all diagrams plots figures dist clean help

# Ordinary builds use the supplied PDFs; figure editors are not required.
all:
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=$(OUT) $(TEX)

diagrams: $(DIAGRAMS:.drawio=.pdf)

figures/diagrams/%.pdf: figures/diagrams/%.drawio Makefile
	$(DRAWIO) --export --format pdf --crop --border 2 --transparent --theme light --output "$@" "$<"

plots:
	$(PYTHON) scripts/plot_results.py

figures: diagrams plots

# An explicit file list keeps local drafts and old exports out of the handoff.
dist: all
	rm -f $(OUT)/provenance-workshop-sources.zip
	zip -q -r $(OUT)/provenance-workshop-sources.zip main.tex Makefile .gitignore requirements.txt tex sections figures scripts $(OUT)/main.pdf -x '*/__pycache__/*' '*.pyc'

clean:
	latexmk -C -outdir=$(OUT) $(TEX)

help:
	@echo 'make          Build build/main.pdf from supplied figures'
	@echo 'make diagrams Export changed .drawio files to cropped vector PDFs'
	@echo 'make plots    Regenerate result plots (pip install -r requirements.txt)'
	@echo 'make figures  Regenerate diagrams and result plots'
	@echo 'make dist     Create build/provenance-workshop-sources.zip'
