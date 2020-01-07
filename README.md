# Parallel Enumerator
Current working build takes in a newline delineated list of IPs and/or domains.

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
### Local
For a list of hosts, run the following from `/path/to/penum.git` directory:
```
./run.sh <HOST_FILE> [<OUTPUT_DIR>] [<NUM_OF_JOBS>]
```

### Docker
Use the following in your Dockerfile to pull the prebuilt image from the Docker Hub:
```
FROM drtychai/penum:latest
```
Alternatively: `docker pull drtychai/penum:latest`

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
