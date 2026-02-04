.PHONY: all
all: install

.PHONY: install
install:
	@pants export
	@ln -sfn dist/export/python/virtualenvs/python-default/*/ venv
	@echo "VENVVV"

.PHONY: clean
clean:
	@rm -f venv
	@echo "VENVVV"
