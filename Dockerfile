FROM python:3.10-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . .
RUN python3 -m venv .venv
RUN .venv/bin/pip install -r requirements/requirements.txt
CMD [".venv/bin/gunicorn", "-w", "4", "choralcat.wsgi", "--bind", "127.0.0.1:8000"]
