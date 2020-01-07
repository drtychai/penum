FROM ubuntu:18.04
ENV DEBIAN_FRONTEND noninteractive

RUN apt update \
    && apt -y install locales
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Create tools directory
RUN mkdir $HOME/tools

# Install base tools
RUN apt update \
    && apt -y install sudo man inetutils-ping locate \
                      netcat socat nmap traceroute dnsutils \
                      gcc g++ libc6-dev make pkg-config \
                      libgmp-dev libmpfr-dev libmpc-dev \
                      git curl wget vim parallel ftp nikto \
                      unzip p7zip chromium-browser tmux jq \
    && apt clean

# Install Languages
## Py2/3
RUN apt update \
    && apt -y install python-dev python-pip virtualenv \
    && apt -y install python3-dev python3-pip python3-venv \
    && apt clean

RUN python -m pip install --upgrade pip \
    && python -m pip install --upgrade setuptools

RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install --upgrade setuptools

## Golang (https://raw.githubusercontent.com/docker-library/golang/master/1.13/buster/Dockerfile)
ENV GOLANG_VERSION 1.13.5
RUN set -eux; \
    \
# this "case" statement is generated via "update.sh"
    dpkgArch="$(dpkg --print-architecture)"; \
    case "${dpkgArch##*-}" in \
        amd64) goRelArch='linux-amd64'; goRelSha256='512103d7ad296467814a6e3f635631bd35574cab3369a97a323c9a585ccaa569' ;; \
        armhf) goRelArch='linux-armv6l'; goRelSha256='26259f61d52ee2297b1e8feef3a0fc82144b666a2b95512402c31cc49713c133' ;; \
        arm64) goRelArch='linux-arm64'; goRelSha256='227b718923e20c846460bbecddde9cb86bad73acc5fb6f8e1a96b81b5c84668b' ;; \
        i386) goRelArch='linux-386'; goRelSha256='3b830fa25f79ab08b476f02c84ea4125f41296b074017b492ac1ff748cf1c7c9' ;; \
        ppc64el) goRelArch='linux-ppc64le'; goRelSha256='292814a5ea42a6fc43e1d1ea61c01334e53959e7ab34de86eb5f6efa9742afb6' ;; \
        s390x) goRelArch='linux-s390x'; goRelSha256='cfbb2959f243880abd1e2efd85d798b8d7ae4a502ab87c4b722c1bd3541e5dc3' ;; \
        *) goRelArch='src'; goRelSha256='27d356e2a0b30d9983b60a788cf225da5f914066b37a6b4f69d457ba55a626ff'; \
            echo >&2; echo >&2 "warning: current architecture ($dpkgArch) does not have a corresponding Go binary release; will be building from source"; echo >&2 ;; \
    esac; \
    \
    url="https://golang.org/dl/go${GOLANG_VERSION}.${goRelArch}.tar.gz"; \
    wget -O go.tgz "$url"; \
    echo "${goRelSha256} *go.tgz" | sha256sum -c -; \
    tar -C /usr/local -xzf go.tgz; \
    rm go.tgz; \
    \
    if [ "$goRelArch" = 'src' ]; then \
        echo >&2; \
        echo >&2 'error: UNIMPLEMENTED'; \
        echo >&2 'TODO install golang-any from jessie-backports for GOROOT_BOOTSTRAP (and uninstall after build)'; \
        echo >&2; \
        exit 1; \
    fi; \
    \
    export PATH="/usr/local/go/bin:$PATH"; \
    go version

ENV GOPATH /go
ENV PATH $GOPATH/bin:/usr/local/go/bin:$PATH

RUN mkdir -p "$GOPATH/src" "$GOPATH/bin" && chmod -R 777 "$GOPATH"


# Install Tools
RUN echo "will cite" | parallel --citation

## Golang tools
### Subfinder
RUN go get -v github.com/projectdiscovery/subfinder/cmd/subfinder

### amass
ENV GO111MODULE on
RUN go get -v -u github.com/OWASP/Amass/v3/...

### aquatone
RUN wget https://github.com/michenriksen/aquatone/releases/download/v1.7.0/aquatone_linux_amd64_1.7.0.zip \
    && unzip aquatone_linux_amd64_1.7.0.zip -d /usr/local/bin \
    && rm aquatone_linux_amd64_1.7.0.zip

## Python tools
### sublist3r
RUN cd $HOME/tools \
    && git clone https://github.com/aboul3la/Sublist3r.git sublist3r && cd sublist3r \
    && python2 -m pip install -r requirements.txt \
    && python2 -m pip install .

### aiodnsbrute
RUN cd $HOME/tools \
    && git clone https://github.com/blark/aiodnsbrute.git && cd aiodnsbrute \
    && curl https://raw.githubusercontent.com/blark/aiodnsbrute/8c9b6514d2f08c344b1cc71490fa074fbabcb90b/aiodnsbrute/cli.py > aiodnsbrute/cli.py \
    && python3 -m pip install .

# Pull penum src and wordlists
RUN cd && git clone https://github.com/drtychai/penum.git
RUN cd && git clone --recurse-submodules https://github.com/drtychai/wordlists.git

WORKDIR /root
