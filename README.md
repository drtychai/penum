# Parallel Enumerator
Current branch still in progress. Only amass container is implemented with bare minimal functionality.

## Overview
Given a file of domain names, the following actions are performed in this order:
1. Initial subdomain discovery via:
    - `subfinder`
    - `sublist3r`
    - `aiodnsbrute`
1. Full subdomain discovery via `amass` using outputs from `1.` as input of known subdomain(s)
1. DNS flyover to discover, screenshot, and output list of HTTP servers via `aquatone`
1. Scan all valid HTTP servers via `nikto`

## Usage
Start all services:
```
docker-compose up
```

This builds and starts all containers with an API exposed at `http://localhost:5000/api/<HOST>`, e.g.,
```
curl http://localhost:5000/api/yahoo.com
```

## Tools
- GNU parallel
- subfinder
- aiodnsbrute
- sublist3r
- amass
- aquatone
- nikto
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
- Fix paths to allow execution from any directory
- Improve container
- Integrate custom recon-ng module
- DB integration
- (Way down the road) Some way of visualizing data
