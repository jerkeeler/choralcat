requires:
	pip-compile requirements/requirements.in
	pip-compile requirements/dev-requirements.in


install:
	pip-sync requirements/requirements.txt

install_dev:
	pip-sync requirements/requirements.txt requirements/dev-requirements.txt
	npm ci

build:
	npm run prod
	DEBUG=True python manage.py collectstatic --noinput

test:
	python manage.py test

load_testdata:
	python manage.py loaddata choralcat/web/fixtures/*
