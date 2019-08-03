SNAPCRAFT := $(shell command -v snapcraft 2>/dev/null)

.PHONY: build
build: # Build snap
ifdef SNAPCRAFT
	snapcraft
else
	docker run \
	       --tty \
	       --volume "$(CURDIR)":/build \
	       --workdir /build \
	       --entrypoint snapcraft \
	       snapcore/snapcraft:stable
endif

.PHONY: lint
lint: lint-shell lint-python # Lint all

.PHONY: lint-shell
lint-shell: # Lint shell scripts
	@docker run --rm --tty --volume "$(CURDIR):/source:ro" inviz/shellcheck

.PHONY: lint-python
lint-python: # Lint Python code
	@docker run --rm --tty --volume "$(CURDIR):/data:ro" cytopia/pycodestyle share

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?# .*$$' ./Makefile | sort | awk \
		'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
