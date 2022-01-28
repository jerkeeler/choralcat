requirements:
	pip-compile requirements.in --generate-hashes --allow-unsafe

install:
	pip install -r requirements.txt
	npm ci

build:
	npm run prod
	DEBUG=True python manage.py collectstatic --noinput

test:
	python manage.py test
