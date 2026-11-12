PYTHON ?= python3
VERSION ?= $(shell git describe --tags --always --dirty 2>/dev/null || echo dev)
LEVEL ?= patch
RELEASE_VERSION ?=
TAGS ?= 0
BUILD_DATE ?= $(shell date -u '+%Y-%m-%d_%H:%M:%S')
PX := $(PYTHON) -m px --root .
VOLUME_SCRIPT := scripts/volumes

.PHONY: all help build volumes vol1 vol2 vol3 generate-vol1 generate-vol2 generate-vol3 clean clean-vols clean-vol1 clean-vol2 clean-vol3 verify test doctor version tags changelog bump tag push

all: build

# The default project build generates and builds all three Workspace documents.
build: clean
	@PYTHON="$(PYTHON)" PROJECT_VERSION="$(VERSION)" BUILD_DATE="$(BUILD_DATE)" bash $(VOLUME_SCRIPT)/build.sh all

volumes: build

vol1: clean-vol1
	@PYTHON="$(PYTHON)" PROJECT_VERSION="$(VERSION)" BUILD_DATE="$(BUILD_DATE)" bash $(VOLUME_SCRIPT)/build.sh vol1

vol2: clean-vol2
	@PYTHON="$(PYTHON)" PROJECT_VERSION="$(VERSION)" BUILD_DATE="$(BUILD_DATE)" bash $(VOLUME_SCRIPT)/build.sh vol2

vol3: clean-vol3
	@PYTHON="$(PYTHON)" PROJECT_VERSION="$(VERSION)" BUILD_DATE="$(BUILD_DATE)" bash $(VOLUME_SCRIPT)/build.sh vol3

generate-vol1:
	@PROJECT_VERSION="$(VERSION)" BUILD_DATE="$(BUILD_DATE)" bash $(VOLUME_SCRIPT)/generate.sh vol1

generate-vol2:
	@PROJECT_VERSION="$(VERSION)" BUILD_DATE="$(BUILD_DATE)" bash $(VOLUME_SCRIPT)/generate.sh vol2

generate-vol3:
	@PROJECT_VERSION="$(VERSION)" BUILD_DATE="$(BUILD_DATE)" bash $(VOLUME_SCRIPT)/generate.sh vol3

clean:
	@$(PX) clean
	@bash $(VOLUME_SCRIPT)/clean.sh all

clean-vols: clean

clean-vol1:
	@$(PX) clean vol1
	@bash $(VOLUME_SCRIPT)/clean.sh vol1

clean-vol2:
	@$(PX) clean vol2
	@bash $(VOLUME_SCRIPT)/clean.sh vol2

clean-vol3:
	@$(PX) clean vol3
	@bash $(VOLUME_SCRIPT)/clean.sh vol3

verify:
	@$(PX) verify
	@$(PYTHON) scripts/verify_volumes.py

test:
	@$(PYTHON) -m unittest discover -s tests -v
	@$(MAKE) verify

doctor:
	@command -v git >/dev/null
	@command -v make >/dev/null
	@command -v python3 >/dev/null
	@command -v latexmk >/dev/null
	@command -v pdflatex >/dev/null
	@command -v biber >/dev/null
	@command -v gix >/dev/null
	@command -v psx >/dev/null
	@$(PYTHON) -c 'from importlib.metadata import version; print("Papyrxis Workspace", version("papyrxis-workspace"))'
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

help:
	@echo "Arliz — three-volume publishing workspace"
	@echo "  make build | volumes                 Build all three Workspace documents"
	@echo "  make vol1 | vol2 | vol3              Build one volume"
	@echo "  make generate-vol1 | generate-vol2 | generate-vol3"
	@echo "  make clean | clean-vol1 | clean-vol2 | clean-vol3"
	@echo "  make verify | test | doctor"
	@echo "  make tags | changelog | bump LEVEL=minor"
	@echo "  make tag RELEASE_VERSION=v1.2.0 | push TAGS=1"

.DEFAULT_GOAL := help
