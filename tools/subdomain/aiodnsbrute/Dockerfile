FROM ubuntu:18.04
ENV TOOL aiodnsbrute
ENV HOME /root
RUN apt update --fix-missing \
    && apt -y install curl xinetd git python3-dev python3-pip jq \
    && apt clean

ENV LC_ALL "C.UTF-8"
ENV LANG "C.UTF-8"

RUN python3 -m pip install --upgrade pip setuptools

RUN git clone https://github.com/blark/aiodnsbrute.git $HOME/$TOOL \
    && curl https://raw.githubusercontent.com/blark/aiodnsbrute/8c9b6514d2f08c344b1cc71490fa074fbabcb90b/aiodnsbrute/cli.py > $HOME/$TOOL/aiodnsbrute/cli.py \
    && python3 -m pip install $HOME/$TOOL

ADD ./resolvers.txt /resolvers.txt
ADD config/run_tool.sh /etc/run_tool.sh
ADD config/main.xinetd /etc/xinetd.d/main
ADD config/run_xinetd.sh /etc/run_xinetd.sh

RUN chmod +x /etc/run_xinetd.sh
RUN chmod +x /etc/run_tool.sh

RUN mkdir /$TOOL && chmod 700 /$TOOL

RUN service xinetd restart
