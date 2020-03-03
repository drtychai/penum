FROM golang:1.14

ENV GOOS linux
ENV GOARCH amd64
ENV GOPATH /go

RUN mkdir /www
COPY ./src/* /www/


WORKDIR /www
CMD ["go", "run", "main.go"]

