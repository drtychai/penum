FROM ubuntu:18.04
RUN apt update --fix-missing \
    && apt -y install nmap xinetd \
    && apt clean

ADD config/run_tool.sh /etc/run_tool.sh
ADD config/main.xinetd /etc/xinetd.d/main
ADD config/run_xinetd.sh /etc/run_xinetd.sh

RUN chmod +x /etc/run_xinetd.sh
RUN chmod +x /etc/run_tool.sh

RUN mkdir /nmap && chmod 700 /nmap

RUN service xinetd restart
