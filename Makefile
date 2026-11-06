PYTHON ?= python3
VERSION ?= $(shell git describe --tags --always --dirty 2>/dev/null || echo dev)
LEVEL ?= patch
RELEASE_VERSION ?=
TAGS ?= 0
BUILD_DATE ?= $(shell date -u '+%Y-%m-%d_%H:%M:%S')
PX := PYTHONPATH=workspace $(PYTHON) -m px --root .
VOLUME_SCRIPT := scripts/volumes

.PHONY: all help sync build volumes vol1 vol2 vol3 generate-vol1 generate-vol2 generate-vol3 clean clean-vols clean-vol1 clean-vol2 clean-vol3 verify test doctor version tags changelog bump tag push cover chapter

all: build

sync:
	@git submodule update --init --recursive workspace
	@test -f workspace/src/sync.sh || { echo "Workspace submodule is missing workspace/src/sync.sh" >&2; exit 1; }
	@python3 -c "import yaml" >/dev/null 2>&1 || { echo "PyYAML is required; run: python3 -m pip install -e workspace" >&2; exit 1; }
	@bash workspace/src/sync.sh

# The default project build always produces every configured volume.
build: clean sync
	@PROJECT_VERSION="$(VERSION)" BUILD_DATE="$(BUILD_DATE)" bash $(VOLUME_SCRIPT)/build.sh all

volumes: build

vol1: sync clean-vol1
	@PROJECT_VERSION="$(VERSION)" BUILD_DATE="$(BUILD_DATE)" bash $(VOLUME_SCRIPT)/build.sh vol1

vol2: sync clean-vol2
	@PROJECT_VERSION="$(VERSION)" BUILD_DATE="$(BUILD_DATE)" bash $(VOLUME_SCRIPT)/build.sh vol2

vol3: sync clean-vol3
	@PROJECT_VERSION="$(VERSION)" BUILD_DATE="$(BUILD_DATE)" bash $(VOLUME_SCRIPT)/build.sh vol3

generate-vol1:
	@bash $(VOLUME_SCRIPT)/generate.sh vol1

generate-vol2:
	@bash $(VOLUME_SCRIPT)/generate.sh vol2

generate-vol3:
	@bash $(VOLUME_SCRIPT)/generate.sh vol3

clean:
	@bash $(VOLUME_SCRIPT)/clean.sh all
	@find . -type f \( -name "*.aux" -o -name "*.log" -o -name "*.out" -o -name "*.toc" -o -name "*.bbl" -o -name "*.blg" -o -name "*.synctex.gz" -o -name "*.fdb_latexmk" -o -name "*.fls" -o -name "*.idx" -o -name "*.ilg" -o -name "*.ind" -o -name "*.run.xml" -o -name "*.bcf" \) -delete 2>/dev/null || true

clean-vols: clean

clean-vol1:
	@bash $(VOLUME_SCRIPT)/clean.sh vol1

clean-vol2:
	@bash $(VOLUME_SCRIPT)/clean.sh vol2

clean-vol3:
	@bash $(VOLUME_SCRIPT)/clean.sh vol3

verify:
	@$(PYTHON) scripts/verify_volumes.py

# Run after make build. CI invokes this after the Pipeline build stage.
test:
	@$(PYTHON) -m unittest discover -s tests -v
	@$(PYTHON) scripts/verify_volumes.py

doctor:
	@command -v git >/dev/null
	@command -v make >/dev/null
	@command -v python3 >/dev/null
	@command -v latexmk >/dev/null
	@command -v pdflatex >/dev/null
	@command -v kpsewhich >/dev/null
	@kpsewhich mathdesign.sty >/dev/null || { echo "Math Design is missing; install TeX Live's texlive-fonts-extra package." >&2; exit 1; }
	@command -v biber >/dev/null
	@command -v gix >/dev/null
	@command -v psx >/dev/null
	@$(PX) doctor
	@psx check --config psx.yml

version:
	@gix version show
	@echo "Build date: $(BUILD_DATE)"

tags:
	@$(PX) tags

changelog:
	@$(PX) changelog --output docs/CHANGELOG.md

bump:
	@$(PYTHON) scripts/check_gix_tags.py
	@gix version bump "$(LEVEL)"

tag:
ifndef RELEASE_VERSION
	$(error RELEASE_VERSION is required: make tag RELEASE_VERSION=v1.2.0)
endif
	@$(PYTHON) scripts/check_gix_tags.py
	@$(PX) tag "$(RELEASE_VERSION)" --sign

push:
	@$(PX) push $(if $(filter 1,$(TAGS)),--tags,)

cover:
	@bash workspace/src/generator/cover.sh workspace.yml

chapter:
	@bash workspace/src/generator/chapter.sh $(ARGS)

help:
	@echo "Arliz — three-volume publishing workspace"
	@echo "  make build | volumes                 Build all three volumes"
	@echo "  make vol1 | vol2 | vol3              Build one volume"
	@echo "  make generate-vol1 | generate-vol2 | generate-vol3"
	@echo "  make clean | clean-vol1 | clean-vol2 | clean-vol3"
	@echo "  make test                            Run checks after make build"
	@echo "  make sync | doctor | verify | version"
	@echo "  make tags | changelog | bump LEVEL=minor"
	@echo "  make tag RELEASE_VERSION=v1.2.0 | push TAGS=1"
	@echo "  make cover | chapter ARGS='...'"

.DEFAULT_GOAL := help
