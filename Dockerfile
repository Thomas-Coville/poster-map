FROM python:3.7-slim

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc
RUN pip install gunicorn

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

ADD . /app

EXPOSE 8000

CMD ["gunicorn", "--config", "./config/gunicorn_config.py", "poster_map:create_app()"]