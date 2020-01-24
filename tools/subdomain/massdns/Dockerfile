FROM ubuntu:18.04
RUN apt update --fix-missing \
    && apt -y install xinetd libldns-dev git build-essential python-dev python-pip \
    && apt clean

# Install massdns
ENV HOME /root
RUN git clone https://github.com/blechschmidt/massdns $HOME/massdns \
    && make -C $HOME/massdns
RUN ln -s $HOME/massdns/bin/massdns /bin/massdns

ADD resolvers.txt /resolvers.txt
ADD subdomains-top1million-110000.txt /wl.txt

ADD config/run_tool.sh /etc/run_tool.sh
ADD config/main.xinetd /etc/xinetd.d/main
ADD config/run_xinetd.sh /etc/run_xinetd.sh

RUN chmod +x /etc/run_xinetd.sh
RUN chmod +x /etc/run_tool.sh

RUN mkdir /massdns && chmod 700 /massdns

RUN service xinetd restart
