FROM ubuntu:18.04

RUN apt-get update -y &&\
    apt-get install -y python3.6 python3-pip python3-dev build-essential &&\
    pip3 install --upgrade setuptools pip wheel

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT ["python3", "./main.py"]