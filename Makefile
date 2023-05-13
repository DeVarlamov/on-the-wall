WORKDIR = api_yamdb
MANAGE = python $(WORKDIR)/manage.py
SHELL := /bin/bash

.PHONY: all

define my_func
	@
	if [ ! $$VIRTUAL_ENV ]; then
		source ./venv/bin/activate
	fi
	echo "*** Виртуальное окружение активировано"
	echo "VIRTUAL_ENV=" $$VIRTUAL_ENV
endef

.ONESHELL:
makemigrations:
	@$(call my_func)
	$(MANAGE) makemigrations

.ONESHELL:
migrate:
	@$(call my_func)
	$(MANAGE) migrate



.ONESHELL:
csv_loader:
	@$(call my_func)
	$(MANAGE) csv_loader

.ONESHELL:
createsuperuser:
	@$(call my_func)
	$(MANAGE) createsuperuser

.ONESHELL:
shell:
	@$(call my_func)
	$(MANAGE) shell

.ONESHELL:
runserver:
	@$(call my_func)
	$(MANAGE) runserver

.ONESHELL:
install:
	@$(call my_func)
	pip install -r requirements.txt

.ONESHELL:
style:
	@$(call my_func)
	black -S -l 79 $(WORKDIR)
	isort $(WORKDIR)
	flake8 $(WORKDIR)
	mypy $(WORKDIR)
