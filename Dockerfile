FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY Pipfile /app/
COPY Pipfile.lock /app/

RUN pip install --upgrade pipenv
RUN pipenv install

