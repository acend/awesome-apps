FROM docker.io/alpine:3.21.3
LABEL maintainer="acend"

ENV PIP_BREAK_SYSTEM_PACKAGES 1
RUN apk --no-cache add curl py3-pip py3-cryptography py3-mysqlclient && \
    pip3 install --no-cache-dir \
        "flask==3.0.3" \
        "Flask-SQLAlchemy==3.1.1" \
        "prometheus-flask-exporter==0.23.0" \
        "kubernetes<=27"

EXPOSE 5000
COPY app/ /app

RUN adduser -D web && \
    chown -R web:root /app && \
    chmod -R 2775 /app && \
    \
    pip3 install --no-cache-dir \
	flake8 pylint pylint-flask pylint-flask-sqlalchemy && \
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
