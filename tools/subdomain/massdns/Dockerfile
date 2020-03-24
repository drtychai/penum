FROM ubuntu:18.04
ENV TOOL massdns
ENV TOOL_OUT output/subdomain
RUN apt update --fix-missing \
    && apt install -y libldns-dev git build-essential python

RUN git clone https://github.com/blechschmidt/massdns.git /${TOOL} \
    && make -C /${TOOL}

FROM ubuntu:18.04
ENV TOOL massdns
RUN apt update --fix-missing \
    && apt -y install xinetd

COPY --from=0 /massdns/bin/${TOOL} /bin/${TOOL}

ADD resolvers.txt /resolvers.txt
ADD subdomains-top1million-110000.txt /wl.txt

ADD config/run_tool.sh /etc/run_tool.sh
ADD config/main.xinetd /etc/xinetd.d/main
ADD config/run_xinetd.sh /etc/run_xinetd.sh

RUN chmod +x /etc/run_xinetd.sh
RUN chmod +x /etc/run_tool.sh

RUN mkdir /${TOOL_OUT} && chmod -R 700 /${TOOL_OUT}

RUN service xinetd restart
