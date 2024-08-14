info: 
	@echo "\n=== Available commands ===\n"
	@egrep '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) |  awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-15s\033[0m %s\n", $$1, $$2}'

init: ## Initialize the project
	@make do-create-venv
	@make do-install-packages

do-create-venv:
	@python3 -m venv .venv

do-install-packages:
	@. .venv/bin/activate; pip install -r requirements.txt

whois: ## Check all domains with whois
	@. .venv/bin/activate; cd scripts && python domain-check-api.py

dnscheck: ## Check all domains if they have a response
	@. .venv/bin/activate; cd scripts && python dnscheck.py

codestyle-check: ## Check all Python scripts code style
	@. .venv/bin/activate; black . --check

codestyle-fix: ## Fix all Python scripts code style
	@. .venv/bin/activate; black .