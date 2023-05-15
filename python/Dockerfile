FROM docker.io/alpine:3.18
LABEL maintainer="acend"

RUN apk --no-cache add py3-pip py3-cryptography py3-mysqlclient curl && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir wheel flask flask_sqlalchemy sqlalchemy \
                                prometheus_flask_exporter "kubernetes<=24"

EXPOSE 5000
COPY app/ /app

RUN adduser -D web && \
    chown -R web:root /app && \
    chmod -R 2775 /app && \
    \
    pip3 install --no-cache-dir flake8 pylint pylint-flask pylint-flask-sqlalchemy && \
    python3 -m compileall /app/*.py && \
    python3 -m compileall /app/libs/*.py && \
    python3 -m compileall /app/libs/labs/*.py && \
    flake8 /app/ && \
    pylint --load-plugins pylint_flask -E /app && \
    pip3 uninstall -y flake8 && \
    pip3 uninstall -y pylint && \
    pip3 uninstall -y pylint-flask && \ 
    pip3 uninstall -y pylint-flask-sqlalchemy

WORKDIR /app
USER web
CMD sleep 10; python3 /app/run.py
