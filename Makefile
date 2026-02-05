PYTHON_VERSION = "3.12"

.PHONY: all
all: install

.PHONY: install
install:
	@pants export
	@ln -sfn dist/export/python/virtualenvs/python-default/$(PYTHON_VERSION).*/ venv
	@echo "Adding venv"

.PHONY: clean
clean:
	@rm -f venv
	@echo "Removing venv"
