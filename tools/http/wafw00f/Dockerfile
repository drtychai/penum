FROM python:3
WORKDIR /

RUN apt update --fix-missing \
    && apt install -y xinetd git jq parallel \
    && apt clean

ENV LC_ALL "C.UTF-8"
ENV LANG "C.UTF-8"

RUN git clone https://github.com/EnableSecurity/wafw00f.git

RUN python3 -m pip install --upgrade pip setuptools \
    && python3 -m pip install /wafw00f/

ADD config/run_tool.sh /etc/run_tool.sh
ADD config/main.xinetd /etc/xinetd.d/main
ADD config/run_xinetd.sh /etc/run_xinetd.sh

RUN chmod +x /etc/run_xinetd.sh
RUN chmod +x /etc/run_tool.sh

RUN service xinetd restart
