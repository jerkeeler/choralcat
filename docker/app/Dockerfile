FROM python:3.10-slim-buster as base
RUN apt-get update && apt-get install -y vim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN groupadd -g 1001 app && useradd -r -u 1001 -g app app-user
USER app-user
WORKDIR /app/code
COPY --chown=app-user:app . .
USER root
RUN python3 -m venv ../venv && ../venv/bin/pip install --no-cache-dir -r requirements/requirements.txt
RUN chown -R app-user:app ../venv
USER app-user

FROM base as dev
RUN ../venv/bin/pip-sync requirements/requirements.txt requirements/dev-requirements.txt
CMD ["../venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM base as prod
CMD ["../venv/bin/gunicorn", "-w", "4", "choralcat.wsgi", "--bind", "0.0.0.0:8000"]
