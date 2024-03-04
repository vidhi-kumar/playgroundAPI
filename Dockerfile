FROM python:3.8.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r ./requirements.txt

RUN apt-get update && \
    apt-get install -y curl

COPY . /app

EXPOSE 8000
