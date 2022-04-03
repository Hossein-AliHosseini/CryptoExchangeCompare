FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN useradd -u 1000 hossein
USER hossein
