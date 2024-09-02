FROM python:3.11-slim

WORKDIR /app

COPY . /app
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry install
RUN poetry shell
# Run the Celery worker
CMD ["celery", "-A", "celery_app.celery", "worker", "--loglevel=info"]
