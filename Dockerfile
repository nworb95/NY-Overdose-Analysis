FROM ubuntu:18.04

WORKDIR /app

RUN apt-get update -y &&\
    apt-get install -y python3.6 python3-pip python3-dev build-essential libpq-dev curl &&\
    pip3 install --upgrade setuptools pip wheel

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -

ENV PATH="$HOME/.poetry/bin:$PATH"
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY poetry.lock pyproject.toml /app/

RUN $HOME/.poetry/bin/poetry config virtualenvs.create false &&\
    $HOME/.poetry/bin/poetry run pip install -U pip && \
    $HOME/.poetry/bin/poetry install --no-ansi --no-dev

COPY . /app

ENTRYPOINT ["python3", "./main.py"]