FROM ubuntu:18.04
ENV HOME /
ENV TOOL_OUT output/subdomain
RUN apt update --fix-missing \
    && apt -y install git xinetd python3-dev python3-pip jq \
    && apt clean

ENV LC_ALL "C.UTF-8"
ENV LANG "C.UTF-8"

WORKDIR ${HOME}
RUN python3 -m pip install --upgrade pip setuptools
RUN git clone https://github.com/lanmaster53/recon-ng \
    && ln -s /recon-ng/recon /recon
RUN git clone https://github.com/infosec-au/altdns

RUN python3 -m pip install -r /recon-ng/REQUIREMENTS
RUN python3 -m pip install -r /altdns/requirements.txt

RUN cd /recon-ng && python3 -m pip install recon
RUN python3 -m pip install /altdns/

ADD config/ng-enum.py /recon-ng/ng-enum.py
ADD config/sortedcombined-knock-dnsrecon-fierce-reconng.txt /wl.txt

ADD config/run_tool.sh /etc/run_tool.sh
ADD config/main.xinetd /etc/xinetd.d/main
ADD config/run_xinetd.sh /etc/run_xinetd.sh

RUN chmod +x /recon-ng/ng-enum.py
RUN chmod +x /etc/run_xinetd.sh
RUN chmod +x /etc/run_tool.sh

RUN mkdir -p /${TOOL_OUT} && chmod -R 700 /${TOOL_OUT}

RUN service xinetd restart
