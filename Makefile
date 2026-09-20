PELICAN ?= pelican
PYTHON ?= python3
PORT ?= 8000

.PHONY: help dev preview html publish check deploy github

help:
	@printf 'make dev [PORT=8000]  Live-reloading local preview\n'
	@printf 'make preview          Build a local preview in output-preview/\n'
	@printf 'make publish          Build production files in output/\n'
	@printf 'make check            Build and validate the production site\n'
	@printf 'make deploy           Publish the pushed pelican commit to Pages\n'

dev:
	$(PELICAN) content -s pelicanconf.py -o output-preview -rl -p $(PORT)

preview html:
	$(PELICAN) content -s pelicanconf.py -o output-preview

publish:
	$(PELICAN) content -s publishconf.py -o output --fatal errors

check: publish
	$(PYTHON) scripts/check_generated.py output

deploy github:
	./scripts/deploy.sh
