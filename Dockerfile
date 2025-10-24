FROM python:3.13.7-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    default-mysql-client \
    netcat-openbsd \
    pkg-config && \
    rm -rf /var/lib/apt/lists*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1


CMD sh -c "\
    until nc -z ${DB_HOST:-db} 3306; do echo 'waiting for db'; sleep 1; done; \
    flask db upgrade || true; \
    exec gunicorn --bind 0.0.0.0:8080 --workers 4 app:app \
    "