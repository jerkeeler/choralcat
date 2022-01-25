install:
	pip install -e .
	npm ci

build:
	npm run prod
	python manage.py collectstatic

test:
	python manage.py test
