# Enumeration Logic
## Overview
The following describe the current two control flows of `penum` api handler:

### A. Provided a hostname, e.g., example.com:
1. Subdomain bruteforce 
  - Async exec of: _amass, recon-ng (via [domain][domain]), subfinder, sublist3r, aiodnsbrute, gobuster_
  - Dedup discovered subdomains
  - Attempt to resolve all subdomain via _massdns_
  - IPv[4,6] resolvable subdomains (i.e., the [valid] "discovered" subdomain) saved to postgresDB

1. Async port scan of subdomains
  - full list fed to _rustscan_ (and thus _nmap_) over TCP:0-65535 
  

### B. Provided an IPv[4,6], e.g., 1.1.1.1:
1. PTR record lookup via python `socket`
1. Continued as described in [A][a]


## Intended Execution Flow
Moving to [dropshot][ds], we plan to integrate data and control flows into a simpler steamlined logic, described as follows:



## Future Work



[domain]: https://github.com/drtychai/domain
[a]: #a-provided-a-hostname-eg-examplecom
[ds]: https://github.com/oxidecomputer/dropshot
