PYTHON = python3
VENV = .venv
VENV_PYTHON = $(VENV)/bin/python

install:
	$(PYTHON) -m venv $(VENV)
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install -r requirements.txt

run:
	$(VENV_PYTHON) main.py

setup: install

clean:
	rm -rf $(VENV)
	rm -rf __pycache__

.PHONY: install run setup clean