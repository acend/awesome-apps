FROM alpine
LABEL maintainer="labz"

COPY app/ /app
RUN apk --no-cache add python3 py3-cryptography && \
    pip3 install --upgrade pip && \
    pip3 install flask flask_sqlalchemy --no-cache-dir && \
    adduser -D web && \
    chown web /app 

WORKDIR /app

USER web
CMD [ "python3", "/app/run.py" ]
