FROM python:3
RUN apt update --fix-missing \
    && apt -y install git xinetd parallel \
    && apt clean

ENV LC_ALL "C.UTF-8"
ENV LANG "C.UTF-8"

RUN python -m pip install --upgrade pip setuptools
RUN git clone https://github.com/maurosoria/dirsearch /dirsearch

ADD wordlists/directory-list-2.3-medium.txt /wl.txt
ADD config/default.conf /dirsearch/default.conf

ADD config/run_tool.sh /etc/run_tool.sh
ADD config/main.xinetd /etc/xinetd.d/main
ADD config/run_xinetd.sh /etc/run_xinetd.sh

RUN chmod +x /etc/run_xinetd.sh
RUN chmod +x /etc/run_tool.sh

RUN service xinetd restart
