# Parallel Enumerator
_This project is still in progress._

The current [master](https://github.com/drtychai/penum/tree/master) branch version performes the
full subdomain enumeration, with JSON output to `./api/logs/subdomains-<tld>.json`

This is an *active* enumerator. We take no responsibility for how or where this is used.

## Overview
Give a host or list of hosts, the following actions are performed in this order:
1. Concurrent subdomain discovery via:
    - `subfinder`
    - `sublist3r`
    - `aiodnsbrute`
    - `gobuster`
    - `recon-ng`
    - `amass`
1. Subdomains resolved via `massDNS` (saved in database)
1. [Not implemented] DNS flyover to discover, screenshot, and output list of HTTP servers via `aquatone`
1. [Not implemented] Scan all valid HTTP servers via `nikto`

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
./penum -d example.com
```
This is equivalent to: `curl -X POST -d "<target_host1>" http://<hostname>[:<port>]`


Enumerate against newline-delineated list of FQDNs/IPs:
```
./penum -f /path/to/file
```
This is equivalent to: `curl -F 'uploadedfile=@/path/to/hosts.txt' http://<hostname>[:<port>]/upload`

View execution log:
```
tail -f api/logs/flask-api.log
```

Custom DB query:
```
psql -U postgres --password postgres -d penum -c "<CUSTOM_QUERY>"
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
- httprobe
- nikto
- nmap
- gobuster
- dirsearch

### Network Enumeration
- nmap

## ToDo
### Network
- Determine if network scans should be performed _after_ subdomain enumeration or _concurrently_ with it
- Detect CIDR/ASN and expand range(s) to separate file for nmap consumption
- Add nmap-parse-output support and sorting logic based on service
- ~Add direct calls to shodan APIs~

### HTTP
- Add in dirsearch/gobuster for inital spidering
- (if possible) Look into possible integration for populating/producing a `.burp` with info

### Misc
- ~Integrate custom recon-ng module~
- DB integration for:
  - ~Subdomain enumeration to DB: Write function that ingests amass JSON output and updates DB~
  - HTTP enumeration
- Map out other core services and their port enumeration tools (e.g., SSH, DNS, SMB, RPC, SMTP, SNMP, etc.)
- (Way down the road) Some way of visualizing data
