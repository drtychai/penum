FROM python:2

RUN apt update --fix-missing \
    && apt install -y xinetd git \
    && apt clean

ENV LC_ALL "C.UTF-8"
ENV LANG "C.UTF-8"

RUN git clone https://github.com/EnableSecurity/wafw00f.git /wafw00f

WORKDIR /wafw00f
RUN pip install --upgrade pip setuptools && \
    python setup.py install

ADD config/run_tool.sh /etc/run_tool.sh
ADD config/main.xinetd /etc/xinetd.d/main
ADD config/run_xinetd.sh /etc/run_xinetd.sh

RUN chmod +x /etc/run_xinetd.sh
RUN chmod +x /etc/run_tool.sh

RUN service xinetd restart
