FROM ubuntu:18.04
RUN apt update --fix-missing \
    && apt -y install curl xinetd git python3-dev python3-pip jq \
    && apt clean

ENV LC_ALL "C.UTF-8"
ENV LANG "C.UTF-8"

RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install --upgrade setuptools

# Install aiodnsbrute
ENV HOME /root
RUN git clone https://github.com/blark/aiodnsbrute.git $HOME/aiodnsbrute && cd $HOME/aiodnsbrute \
    && curl https://raw.githubusercontent.com/blark/aiodnsbrute/8c9b6514d2f08c344b1cc71490fa074fbabcb90b/aiodnsbrute/cli.py > aiodnsbrute/cli.py \
    && python3 -m pip install .

ADD ./resolvers.txt /resolvers.txt
ADD config/run_tool.sh /etc/run_tool.sh
ADD config/main.xinetd /etc/xinetd.d/main
ADD config/run_xinetd.sh /etc/run_xinetd.sh

RUN chmod +x /etc/run_xinetd.sh
RUN chmod +x /etc/run_tool.sh

RUN mkdir /aiodnsbrute && chmod 700 /aiodnsbrute

RUN service xinetd restart
