FROM golang:1.13.1
ENV GOOS linux
ENV GOARCH amd64
ENV GOPATH /go
RUN go get -v github.com/michenriksen/aquatone/

FROM ubuntu:18.04
ENV TOOL aquatone
RUN apt update --fix-missing \
    && apt install -y xinetd chromium-browser jq

COPY --from=0 /go/bin/${TOOL} /bin/${TOOL}

ADD config/run_tool.sh /etc/run_tool.sh
ADD config/main.xinetd /etc/xinetd.d/main
ADD config/run_xinetd.sh /etc/run_xinetd.sh

RUN chmod +x /etc/run_xinetd.sh
RUN chmod +x /etc/run_tool.sh

RUN service xinetd restart
