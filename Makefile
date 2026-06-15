MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help
.DELETE_ON_ERROR:
.SUFFIXES:
.SECONDARY:

RUN = poetry run
# get values from about.yaml file
SCHEMA_NAME = $(shell ${SHELL} ./utils/get-value.sh name)
SOURCE_SCHEMA_PATH = $(shell ${SHELL} ./utils/get-value.sh source_schema_path)
SOURCE_SCHEMA_DIR = $(dir $(SOURCE_SCHEMA_PATH))
SRC = src
DEST = project
PYMODEL = $(SRC)/$(SCHEMA_NAME)/datamodel
DOCDIR = docs
EXAMPLEDIR = examples
SHEET_MODULE = personinfo_enums
SHEET_ID = $(shell ${SHELL} ./utils/get-value.sh google_sheet_id)
SHEET_TABS = $(shell ${SHELL} ./utils/get-value.sh google_sheet_tabs)
SHEET_MODULE_PATH = $(SOURCE_SCHEMA_DIR)/$(SHEET_MODULE).yaml

# environment variables
GEN_PARGS =
ifdef LINKML_COOKIECUTTER_GEN_PROJECT_ARGS
GEN_PARGS = ${LINKML_COOKIECUTTER_GEN_PROJECT_ARGS}
endif

GEN_DARGS =
ifdef LINKML_COOKIECUTTER_GEN_DOC_ARGS
GEN_DARGS = ${LINKML_COOKIECUTTER_GEN_DOC_ARGS}
endif


# basename of a YAML file in model/
.PHONY: all clean

# note: "help" MUST be the first target in the file,
# when the user types "make" they should get help info
help: status
	@echo ""
	@echo "make setup -- initial setup (run this first)"
	@echo "make site -- makes site locally"
	@echo "make install -- install dependencies"
	@echo "make test -- runs tests"
	@echo "make lint -- perfom linting"
	@echo "make testdoc -- builds docs and runs local test server"
	@echo "make deploy -- deploys site"
	@echo "make update -- updates linkml version"
	@echo "make help -- show this help"
	@echo ""

status: check-config
	@echo "Project: $(SCHEMA_NAME)"
	@echo "Source: $(SOURCE_SCHEMA_PATH)"

# generate products and add everything to github
setup: install gen-project gen-examples gendoc git-init-add

# install any dependencies required for building
install:
	git init     # issues/33
	poetry install --no-root
.PHONY: install

# ---
# Project Syncronization
# ---
#
# check we are up to date
check: cruft-check
cruft-check:
	cruft check
cruft-diff:
	cruft diff

update: update-template update-linkml
update-template:
	cruft update

# todo: consider pinning to template
update-linkml:
	poetry add -D linkml@latest

# EXPERIMENTAL
create-data-harmonizer:
	npm init data-harmonizer $(SOURCE_SCHEMA_PATH)

all: site
site: gen-project gendoc
%.yaml: gen-project
deploy: all mkd-gh-deploy

compile-sheets:
	$(RUN) sheets2linkml --gsheet-id $(SHEET_ID) $(SHEET_TABS) > $(SHEET_MODULE_PATH).tmp && mv $(SHEET_MODULE_PATH).tmp $(SHEET_MODULE_PATH)

# In future this will be done by conversion
gen-examples:
	mkdir -p $(EXAMPLEDIR)
	cp -r src/data/examples/* $(EXAMPLEDIR)

# generates all project files

gen-project: $(PYMODEL) compile-sheets
	$(RUN) gen-project ${GEN_PARGS} -d $(DEST) $(SOURCE_SCHEMA_PATH) && mv $(DEST)/*.py $(PYMODEL)


# =========================================================================
# Model Card AI Assistant: rubric evaluation
# =========================================================================
# Defaults — override on the command line:
#   make evaluate-rubric10 MC_INPUT_GLOB='src/data/examples/extended/*.yaml'
#   make evaluate-rubric10 MC_INPUT=path/to/card.yaml MC_EVAL_DIR=tmp/eval
MC_INPUT_GLOB ?= src/data/examples/extended/*.yaml
MC_EVAL_DIR   ?= data/evaluation/rubric10

# Hybrid (rule-based + quality heuristics) — fast, no LLM cost
evaluate-rubric10:
ifdef MC_INPUT
	$(RUN) python scripts/batch_evaluate_mc_rubric10_hybrid.py \
		--input  $(MC_INPUT) \
		--output-dir $(MC_EVAL_DIR)
else
	$(RUN) python scripts/batch_evaluate_mc_rubric10_hybrid.py \
		--input-glob '$(MC_INPUT_GLOB)' \
		--output-dir $(MC_EVAL_DIR)
endif

# Smoke-test the hybrid evaluator against the canonical extended example
evaluate-rubric10-smoke:
	$(RUN) python scripts/batch_evaluate_mc_rubric10_hybrid.py \
		--input src/data/examples/extended/climate-model-extended.yaml \
		--output-dir tmp/mc-eval-smoke

# Completeness quality gate (used by the @mcassistant workflow before PR)
#   make check-completeness MC_FILE=path/to/card.yaml [MC_BLOCK=acceptable]
MC_BLOCK ?= minimal
check-completeness:
ifndef MC_FILE
	$(error MC_FILE is required: make check-completeness MC_FILE=path/to/card.yaml)
endif
	$(RUN) python src/github/validate_mc_completeness.py $(MC_FILE) --block-threshold $(MC_BLOCK)

# Prerequisites check for the @mcassistant workflow
#   make check-prereqs MC_MODEL=climatenet MC_MODE=url MC_URLS='https://...'
MC_MODE  ?= url
MC_URLS  ?=
check-prereqs:
ifndef MC_MODEL
	$(error MC_MODEL is required: make check-prereqs MC_MODEL=name MC_MODE=url MC_URLS='https://...')
endif
	@if [ "$(MC_MODE)" = "url" ]; then \
		src/github/validate_prerequisites.sh --model $(MC_MODEL) --mode url --urls "$(MC_URLS)"; \
	else \
		src/github/validate_prerequisites.sh --model $(MC_MODEL) --mode file; \
	fi

MC_EVAL20_DIR ?= data/evaluation/rubric20

evaluate-rubric20:
ifdef MC_INPUT
	$(RUN) python scripts/batch_evaluate_mc_rubric20_hybrid.py \
		--input $(MC_INPUT) \
		--output-dir $(MC_EVAL20_DIR)
else
	$(RUN) python scripts/batch_evaluate_mc_rubric20_hybrid.py \
		--input-glob '$(MC_INPUT_GLOB)' \
		--output-dir $(MC_EVAL20_DIR)
endif

evaluate-rubric20-smoke:
	$(RUN) python scripts/batch_evaluate_mc_rubric20_hybrid.py \
		--input src/data/examples/extended/climate-model-extended.yaml \
		--output-dir tmp/mc-rubric20-smoke

# Render evaluation JSON(s) to HTML
#   make render-eval EVAL_JSONS='tmp/mc-eval-smoke/*.json' EVAL_HTML=tmp/report.html
EVAL_HTML ?= data/evaluation/report.html
render-eval:
ifndef EVAL_JSONS
	$(error EVAL_JSONS is required: make render-eval EVAL_JSONS='glob/of/*.json' EVAL_HTML=path/to/report.html)
endif
	$(RUN) python scripts/render_evaluation_html.py --input-glob '$(EVAL_JSONS)' --output $(EVAL_HTML)

# Cross-evaluator comparison view (hybrid vs LLM × rubric10 / rubric20)
#   make render-compare EVAL_JSONS='glob/of/*.json' EVAL_HTML=path/to/compare.html
render-compare:
ifndef EVAL_JSONS
	$(error EVAL_JSONS is required: make render-compare EVAL_JSONS='glob/of/*.json' EVAL_HTML=path/to/compare.html)
endif
	$(RUN) python scripts/render_evaluation_html.py --input-glob '$(EVAL_JSONS)' --output $(EVAL_HTML) --compare --title "Cross-evaluator comparison"

# Emit shields.io-style SVG quality badges (one per evaluation) + index.html
#   make render-badges EVAL_JSONS='glob/of/*.json' BADGE_DIR=data/evaluation/badges
BADGE_DIR ?= data/evaluation/badges
render-badges:
ifndef EVAL_JSONS
	$(error EVAL_JSONS is required: make render-badges EVAL_JSONS='glob/of/*.json' [BADGE_DIR=path/])
endif
	$(RUN) python scripts/render_evaluation_html.py --input-glob '$(EVAL_JSONS)' --output $(BADGE_DIR) --badge --title "Model Card quality badges"

.PHONY: evaluate-rubric10 evaluate-rubric10-smoke evaluate-rubric20 evaluate-rubric20-smoke check-completeness check-prereqs render-eval render-compare render-badges

test: test-schema test-python test-examples

test-schema:
	$(RUN) gen-project ${GEN_PARGS} -d tmp $(SOURCE_SCHEMA_PATH)

test-python:
	$(RUN) python -m unittest discover

lint:
	$(RUN) linkml-lint $(SOURCE_SCHEMA_PATH)

check-config:
	@(grep my-datamodel about.yaml > /dev/null && printf "\n**Project not configured**:\n\n  - Remember to edit 'about.yaml'\n\n" || exit 0)

convert-examples-to-%:
	$(patsubst %, $(RUN) linkml-convert  % -s $(SOURCE_SCHEMA_PATH) -C Person, $(shell ${SHELL} find src/data/examples -name "*.yaml"))

examples/%.yaml: src/data/examples/%.yaml
	$(RUN) linkml-convert -s $(SOURCE_SCHEMA_PATH) -C Person $< -o $@
examples/%.json: src/data/examples/%.yaml
	$(RUN) linkml-convert -s $(SOURCE_SCHEMA_PATH) -C Person $< -o $@
examples/%.ttl: src/data/examples/%.yaml
	$(RUN) linkml-convert -P EXAMPLE=http://example.org/ -s $(SOURCE_SCHEMA_PATH) -C Person $< -o $@

test-examples: examples/output

examples/output: $(SOURCE_SCHEMA_PATH)
	mkdir -p $@
	$(RUN) linkml-run-examples \
		--output-formats json \
		--output-formats yaml \
		--counter-example-input-directory src/data/examples/invalid \
		--input-directory src/data/examples/valid \
		--output-directory $@ \
		--schema $< > $@/README.md

# Test documentation locally
serve: mkd-serve

# Python datamodel
$(PYMODEL):
	mkdir -p $@


$(DOCDIR):
	mkdir -p $@

gendoc: $(DOCDIR)
	cp $(SRC)/docs/*md $(DOCDIR) ; \
	$(RUN) gen-doc ${GEN_DARGS} -d $(DOCDIR) $(SOURCE_SCHEMA_PATH)

testdoc: gendoc serve

MKDOCS = $(RUN) mkdocs
mkd-%:
	$(MKDOCS) $*

PROJECT_FOLDERS = sqlschema shex shacl protobuf prefixmap owl jsonschema jsonld graphql excel
git-init-add: git-init git-add git-commit git-status
git-init:
	git init
git-add: .cruft.json
	git add .gitignore .github .cruft.json Makefile LICENSE *.md examples utils about.yaml mkdocs.yml poetry.lock project.Makefile pyproject.toml src/linkml/*yaml src/*/datamodel/*py src/data src/docs tests src/*/_version.py
	git add $(patsubst %, project/%, $(PROJECT_FOLDERS))
git-commit:
	git commit -m 'chore: initial commit' -a
git-status:
	git status

# only necessary if setting up via cookiecutter
.cruft.json:
	echo "creating a stub for .cruft.json. IMPORTANT: setup via cruft not cookiecutter recommended!" ; \
	touch $@

clean:
	rm -rf $(DEST)
	rm -rf tmp
	rm -fr docs/*

include project.Makefile
