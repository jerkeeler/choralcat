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
	autoflake choralcat/ -c -r --ignore-init-module-imports --remove-all-unused-imports
	isort choralcat/ --profile black --check
	black choralcat/ --check --line-length 120
	mypy choralcat/

mypy:
	mypy choralcat/

test:
	python manage.py test --parallel

load_testdata:
	python manage.py loaddata choralcat/web/fixtures/*

docker_build:
	docker build . --tag jerkeeler/choralcat:app-dev -f docker/app/Dockerfile --target dev
	docker build . --tag jerkeeler/choralcat:caddy-dev -f docker/caddy/Dockerfile

dock_down:
	docker-compose -f docker/docker-compose.yml --project-directory . down

dock_up:
	docker-compose -f docker/docker-compose.yml --project-directory . up -d

dock_migrate:
	docker-compose -f docker/docker-compose.yml --project-directory . run app ../venv/bin/python manage.py migrate
