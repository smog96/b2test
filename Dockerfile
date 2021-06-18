FROM python:3.9.5-slim

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp