FROM python:3.9.5-slim

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt
