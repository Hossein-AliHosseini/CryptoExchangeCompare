FROM python:3.8

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

ADD . /cryptoexchangecompare
WORKDIR /cryptoexchangecompare

RUN useradd -u 1000 hossein
USER hossein
