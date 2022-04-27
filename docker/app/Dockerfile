FROM python:3.10-slim-buster as base
RUN apt-get update && apt-get install -y vim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN addgroup --system web && adduser --system --ingroup web web
USER web
WORKDIR /home/web/app
COPY --chown=web:web . .
USER root
RUN python3 -m venv ../venv && ../venv/bin/pip install --no-cache-dir -r requirements/requirements.txt
RUN chown -R web:web ../venv
USER web

FROM base as dev
RUN ../venv/bin/pip-sync requirements/requirements.txt requirements/dev-requirements.txt
CMD ["../venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM base as prod
CMD ["../venv/bin/gunicorn", "-w", "4", "choralcat.wsgi", "--bind", "0.0.0.0:8000"]
