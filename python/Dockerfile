FROM alpine
LABEL maintainer="acend"

EXPOSE 5000
COPY app/ /app

RUN apk --no-cache add py3-pip py3-cryptography py3-mysqlclient curl && \
    pip3 install --upgrade pip && \
    pip3 install flask flask_sqlalchemy prometheus_flask_exporter kubernetes flake8 --no-cache-dir && \
    \
    adduser -D web && \
    chown -R web:root /app && \
    chmod -R 2775 /app && \
    \
    python3 -m compileall /app/*.py && \
    python3 -m compileall /app/libs/*.py && \
    flake8 /app/

WORKDIR /app
USER web
CMD sleep 10; python3 /app/run.py
