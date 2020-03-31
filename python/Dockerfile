FROM alpine
LABEL maintainer="labz"

RUN apk --no-cache add python3 py3-cryptography && \
    pip3 install --upgrade pip && \
    pip3 install flask flask_sqlalchemy --no-cache-dir && \
    adduser -D web

COPY run.py /

USER web
CMD [ "python3", "run.py" ]
