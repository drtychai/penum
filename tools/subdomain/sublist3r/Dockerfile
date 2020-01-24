FROM ubuntu:18.04
RUN apt update --fix-missing \
    && apt -y install curl xinetd git python-dev python-pip \
    && apt clean

ENV LC_ALL "C.UTF-8"
ENV LANG "C.UTF-8"

RUN python -m pip install --upgrade pip \
    && python -m pip install --upgrade setuptools

# Install sublist3r
ENV HOME /root
RUN git clone https://github.com/aboul3la/Sublist3r.git $HOME/sublist3r && cd $HOME/sublist3r \
    && python -m pip install -r requirements.txt \
    && python -m pip install .

ADD config/run_tool.sh /etc/run_tool.sh
ADD config/main.xinetd /etc/xinetd.d/main
ADD config/run_xinetd.sh /etc/run_xinetd.sh

RUN chmod +x /etc/run_xinetd.sh
RUN chmod +x /etc/run_tool.sh

RUN mkdir /sublist3r && chmod 700 /sublist3r

RUN service xinetd restart
