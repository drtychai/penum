FROM golang:1.16.2
ENV GO111MODULE=on \
    GOOS=linux \
    GOARCH=amd64 \
    GOPATH=/go
RUN go get -v github.com/OWASP/Amass/v3/...

FROM ubuntu:18.04
ENV TOOL=amass \
    TOOL_OUT=/output/subdomain \
    LOG_OUT=/log

RUN apt update --fix-missing \
    && apt install -y xinetd

COPY --from=0 /go/bin/${TOOL} /bin/${TOOL}

ADD config/config_template.ini /config_template.ini
ADD config/run_tool.sh /etc/run_tool.sh
ADD config/main.xinetd /etc/xinetd.d/main
ADD config/run_xinetd.sh /etc/run_xinetd.sh

RUN chmod +x /etc/run_xinetd.sh \
    && chmod +x /etc/run_tool.sh

RUN mkdir -p ${TOOL_OUT} ${LOG_OUT} \
    && chmod -R 700 ${TOOL_OUT} \
    && chmod -R 700  ${LOG_OUT}

RUN service xinetd restart
