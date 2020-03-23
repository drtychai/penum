# Parallel Enumerator
Current branch still in progress. Functionality is equivalent to `master`.

This is an *active* enumerator. We take no responsibility for how or where this is used.

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
docker-compose up -d
```

To stop all service and *preserve* the database:
```
docker-compose down
```

To stop all service and *destroy* the database:
```
docker-compose down -v
```

Backend functionality is queried through the Golang HTTP server at: `http://localhost:8080`

### Specific Functionality
Enumerate against single FQDN/IP:
```
curl -X POST -d "<target_host1>" http://<hostname>[:<port>]
```

Enumerate against newline-delineated list of FQDNs/IPs:
```
curl -F 'uploadedfile=@/path/to/hosts.txt' http://<hostname>[:<port>]/upload
```

Custom DB query:
```
psql -U postgres -d penum -c "<CUSTOM_QUERY>"
```


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
  - Create converter per tools output into DB JSON syntax
- (Way down the road) Some way of visualizing data
