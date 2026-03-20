.PHONY: sync-refs check-refs install uninstall reinstall setup-hooks

sync-refs:
	python3 workflow/scripts/resolve-refs.py

check-refs:
	python3 workflow/scripts/resolve-refs.py --check

install: sync-refs
	claude plugins uninstall look-before-you-leap --scope user 2>/dev/null || true
	claude plugins install look-before-you-leap --scope user

uninstall:
	claude plugins uninstall look-before-you-leap --scope user

reinstall: install

setup-hooks:
	git config core.hooksPath .githooks
