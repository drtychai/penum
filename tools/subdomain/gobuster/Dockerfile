FROM golang:1.13.7
ENV GO111MODULE on
ENV GOOS linux
ENV GOARCH amd64
ENV GOPATH /go
RUN go get -v -u github.com/OJ/gobuster/...

FROM ubuntu:18.04
ENV TOOL gobuster
RUN apt update --fix-missing \
    && apt -y install xinetd \
    && apt clean

COPY --from=0 /go/bin/$TOOL /bin/$TOOL

ADD config/run_tool.sh /etc/run_tool.sh
ADD config/main.xinetd /etc/xinetd.d/main
ADD config/run_xinetd.sh /etc/run_xinetd.sh

RUN chmod +x /etc/run_xinetd.sh
RUN chmod +x /etc/run_tool.sh

RUN mkdir /$TOOL && chmod 700 /$TOOL

RUN service xinetd restart
