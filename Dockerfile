FROM python:3.8

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN mkdir /cryptoexchangecompare
WORKDIR /cryptoexchangecompare
COPY ./cryptoexchangecompare /cryptoexchangecompare

