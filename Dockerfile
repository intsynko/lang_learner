FROM python:3.10

## install dependencies for psycopg2
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

RUN mkdir /app
WORKDIR /app
RUN pip install poetry
COPY poetry.lock pyproject.toml /app/
ENV DJANGO_SETTINGS_MODULE=settings.production
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi
COPY app /app/
RUN python manage.py collectstatic
