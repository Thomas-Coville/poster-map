FROM python:3.7-slim

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

ADD . /app

CMD ["gunicorn", "--config", "./config/gunicorn_config.py", "main:app"]