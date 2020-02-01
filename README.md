# Parallel Enumerator
Current branch still in progress. Functionality is equivalent to `master`.

This is an *active* enumerator. We take no responsibility for how this is used.

## Overview
Give a host or list of hosts, the following actions are performed in this order:
1. Concurrent subdomain discovery via:
    - `subfinder`
    - `sublist3r`
    - `aiodnsbrute`
    - `gobuster`
    - `amass`
1. DNS flyover to discover, screenshot, and output list of HTTP servers via `aquatone`
1. Scan all valid HTTP servers via `nikto`

## Installation
penum requires `docker` and `docker-compose` be installed on the host.
- Linux
  `sudo apt -y install docker docker-compose`
- macOS
  `brew install docker && brew cask install docker`

## Usage
From the root of this repository, start all services:
```
docker-compose up
```

This builds and starts all containers with an API endpoint at `http://localhost:5000/api`.

### Specific Functionality
Run the core of penum:

```curl -X POST -H "Content-Type: application/json" -d '{"hosts":["<target_host1>","<target_host2>",...,"<target_hostN>"]}' http://<hostname>[:<port>]/api```

Run specific tool:

```curl -X POST -H "Content-Type: application/json" -d '{"hosts":["<target_host1>","<target_host2>",...,"<target_hostN>"]}' http://<hostname>[:<port>]/api/<tool>```

Get all results:

```curl -X POST -H "Content-Type: application/json" -d '{"hosts":["<target_host1>","<target_host2>",...,"<target_hostN>"]}' http://<hostname>[:<port>]/api/output```

Get specific tool results:

```curl -X POST -H "Content-Type: application/json" -d '{"hosts":["<target_host1>","<target_host2>",...,"<target_hostN>"]}' http://<hostname>[:<port>]/api/output/<tool>```

## Tools used
### Subdomain Enumeration
- subfinder
- aiodnsbrute
- sublist3r
- amass
- gobuster
- massDNS
- recon-NG

### HTTP Enumeration
- aquatone
- nikto
- nmap

### Network Enumeration
- nmap

## ToDo
### Network
- Detect CIDR/ASN and expand range(s) to separate file for nmap consumption
- Add nmap-parse-output support and sorting logic based on service
- Add direct calls to shodan APIs

### HTTP
- Add in dirsearch/gobuster for inital spidering
- (if possible) Look into possible integration for populating/producing a `.burp` with info

### Misc
- Integrate custom recon-ng module
- DB integration
- (Way down the road) Some way of visualizing data
