PELICAN ?= pelican
PYTHON ?= python3
PORT ?= 8000

.PHONY: help html dev publish check

help:
	@printf 'make dev [PORT=8000]  Live-reloading local preview\n'
	@printf 'make html             Build the local site in output/\n'
	@printf 'make publish          Build production files in output/\n'
	@printf 'make check            Build and validate the production site\n'

dev:
	$(PELICAN) content -s pelicanconf.py -lr -p $(PORT)

html:
	$(PELICAN) content -s pelicanconf.py

publish:
	$(PELICAN) content -s publishconf.py --fatal warnings

check: publish
	$(PYTHON) scripts/check_generated.py output
