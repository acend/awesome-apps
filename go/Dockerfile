FROM golang:1.13
COPY main.go /go
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build 

FROM alpine
LABEL maintainer="labz"
EXPOSE 5000
COPY --from=0 /go/go /usr/local/bin/
RUN adduser -D web

USER web
CMD [ "/usr/local/bin/go" ]
