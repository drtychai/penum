FROM ubuntu:18.04
ENV TOOL sublist3r
ENV HOME /root
RUN apt update --fix-missing \
    && apt -y install curl xinetd git python-dev python-pip \
    && apt clean

ENV LC_ALL "C.UTF-8"
ENV LANG "C.UTF-8"

RUN python -m pip install --upgrade pip setuptools

RUN git clone https://github.com/aboul3la/Sublist3r.git $HOME/$TOOL \
    && python -m pip install -r $HOME/$TOOL/requirements.txt \
    && python -m pip install $HOME/$TOOL

ADD config/run_tool.sh /etc/run_tool.sh
ADD config/main.xinetd /etc/xinetd.d/main
ADD config/run_xinetd.sh /etc/run_xinetd.sh

RUN chmod +x /etc/run_xinetd.sh
RUN chmod +x /etc/run_tool.sh

RUN mkdir /$TOOL && chmod 700 /$TOOL

RUN service xinetd restart
