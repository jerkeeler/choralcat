FROM python:3.10-slim-buster
RUN apt-get update && apt-get install -y vim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . .
RUN python3 -m venv .venv && .venv/bin/pip install -r requirements/requirements.txt
CMD [".venv/bin/gunicorn", "-w", "4", "choralcat.wsgi", "--bind", "0.0.0.0:8000"]
