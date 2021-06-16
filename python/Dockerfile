FROM alpine:3.13
LABEL maintainer="acend"


RUN apk --no-cache add py3-pip py3-cryptography py3-mysqlclient curl && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir flask \
                                flask_sqlalchemy \
				prometheus_flask_exporter \
				flake8 \
                 		"sqlalchemy<1.4" \
		 		kubernetes

EXPOSE 5000
COPY app/ /app

RUN adduser -D web && \
    chown -R web /app && \
    \
    python3 -m compileall /app/*.py && \
    python3 -m compileall /app/libs/*.py && \
    flake8 /app/

WORKDIR /app
USER web
CMD sleep 10; python3 /app/run.py
