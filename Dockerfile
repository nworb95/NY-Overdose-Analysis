FROM python:3.6.1-alpine

run apt-get update \
      && apt-get install \
      build-base \
      postgresql \
      postgresql-dev \
      libpq
