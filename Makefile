help:
	@echo "setenv          setup new env dep"
	@echo "sync            sync a fork from upstream "
	@echo "pre-commit      install pre-commit in .git dir"
	@echo "check-all       check all files"

setenv:
	pip install -r requirements.txt -r requirements-dev.txt

sync:
	git checkout main && git pull origin main

pre-commit:
	pre-commit install --hook-type commit-msg --hook-type pre-commit --overwrite

check-all:
	pre-commit run --all-files
