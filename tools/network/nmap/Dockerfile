FROM ubuntu:18.04
ENV TOOL nmap
RUN apt update --fix-missing \
    && apt -y install $TOOL xinetd \
    && apt clean

ADD config/run_tool.sh /etc/run_tool.sh
ADD config/main.xinetd /etc/xinetd.d/main
ADD config/run_xinetd.sh /etc/run_xinetd.sh

RUN chmod +x /etc/run_xinetd.sh
RUN chmod +x /etc/run_tool.sh

RUN mkdir /$TOOL && chmod 700 /$TOOL

RUN service xinetd restart
