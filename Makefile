requires:
	pip-compile requirements/requirements.in
	pip-compile requirements/dev-requirements.in


install:
	.venv/bin/pip-sync requirements/requirements.txt

install_dev:
	pip install pip-tools==6.5.0
	pip-sync requirements/requirements.txt requirements/dev-requirements.txt
	npm ci

build:
	npm run prod
	DEBUG=True python manage.py collectstatic --noinput

check:
	black choralcat/ --check
	isort choralcat/ --profile black --check

test:
	python manage.py test

load_testdata:
	python manage.py loaddata choralcat/web/fixtures/*
