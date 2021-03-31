FROM golang:1.16.2
ENV GO111MODULE=on \
    GOOS=linux \
    GOARCH=amd64 \
    GOPATH=/go 
RUN go get -v -u github.com/projectdiscovery/subfinder/v2/cmd/subfinder

FROM ubuntu:18.04
ENV TOOL subfinder
ENV TOOL_OUT output/subdomain
RUN apt update --fix-missing \
    && apt -y install xinetd \
    && apt clean

COPY --from=0 /go/bin/${TOOL} /bin/${TOOL}

ADD config/run_tool.sh /etc/run_tool.sh
ADD config/main.xinetd /etc/xinetd.d/main
ADD config/run_xinetd.sh /etc/run_xinetd.sh

RUN chmod +x /etc/run_xinetd.sh
RUN chmod +x /etc/run_tool.sh

RUN mkdir -p /${TOOL_OUT} && chmod -R 700 /${TOOL_OUT}

RUN service xinetd restart
