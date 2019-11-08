FROM python:3.7.5-slim-buster

RUN apt-get update \
    && apt-get -y install curl build-essential libssl-dev \
    && apt-get clean \
    && pip3 install --upgrade pip


RUN mkdir /lazy-nicehash
WORKDIR /lazy-nicehash


ENV LD_LIBRARY_PATH /usr/local/lib


COPY requirements.txt /lazy-nicehash/
RUN pip3 install -r requirements.txt --no-cache-dir


COPY . /lazy-nicehash/


CMD [ "python3", "./bot.py" ]
