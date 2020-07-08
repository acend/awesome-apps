FROM alpine
LABEL maintainer="acend"

COPY app/ /app
RUN apk --no-cache add py3-pip py3-cryptography py3-mysqlclient curl && \
    pip3 install --upgrade pip && \
    pip3 install flask flask_sqlalchemy prometheus_flask_exporter --no-cache-dir && \
    adduser -D web && \
    chown web /app 

WORKDIR /app

USER web
CMD sleep 10; python3 /app/run.py
