#!/usr/bin/env python3
from dns import resolver, reversename
from multiprocessing import Pool
import psql_helper
import socket
import re

def tool_port_map(tool):
    mapping = {"amass":30000,
               "subfinder":30001,
               "aiodnsbrute":30002,
               "sublist3r":30003,
               "gobuster":30004,
               "massdns":30005,
               "recon-ng":30006,
               "aquatone":30007,
               "httprobe":30008,
               "wart":30009,
               "nmap":30010}
    return mapping[f"{tool}"]

def start_proc(tool, host, logger, pool):
    logger.debug(f"[*] Starting {tool} on {host}...")
    return pool.apply_async(run_service, args=(tool, host, logger))

def run_service(tool, host, logger):
    """Run service and copy output from tool's container."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((tool, tool_port_map(tool)))

    # Send host
    payload = bytes(f"{host}\n", encoding='utf-8')
    s.send(payload)

    output = b''
    while True:
        chunk = s.recv(2048)
        if b"DONE" in chunk:
            logger.debug(f"[*] {tool} FINISHED...")
            break
    return

def check_cache(host):
    """Checks if host has already been enumerated. Return boolean."""
    result = False
    # TODO: check if file names exists
    return result

def port_scan(host):
    """"Main controller for IP / Network enumeration."""
    pool = Pool()
    start_proc("nmap", host, None, pool)
    return

def reverseDNS(addr):
    qname = reversename.from_address(addr)
    return str(resolver.query(qname, 'PTR')[0])[:-1]

def find_subdomains(host, logger):
    """Main controller for subdomain enumeration tools."""

    # Check if db is initialized
    if not psql_helper.is_init():
        psql_helper.init()

    pool = Pool()
    procs = []
    tools = ["amass", "recon-ng",
             "subfinder", "sublist3r",
             "aiodnsbrute", "gobuster"]

    logger.info("\033[0m-"*50)
    logger.info("[+] Launching wave one...")
    for tool in tools:
        p = start_proc(tool, host, logger, pool)
        procs.append(p)

    # wait until all pool processes complete
    for proc in procs:
        proc.get()

    # use massdns to filter non-resolvable subdomains
    p = start_proc("massdns", host, logger, pool)
    p.get()

    # update db with amass output
    psql_helper.update_subdomains(f"/output/subdomain/subdomains-{host}.json", logger)
    logger.debug(f"[*] Database update complete...")
    return

def http_enum(host, logger):
    """Main controler for HTTP enumeration tools."""
    pool = Pool()
    procs = []
    tools = ["aquatone", "httprobe"]

    logger.info("[+] Beginning HTTP enumeration...")
    for tool in tools:
        p = start_proc(tool, host, logger, pool)
        procs.append(p)

    for proc in procs:
        proc.get()

    # Combine and sort enumerated webservers
    p = re.compile(r'/.*.[A-Za-z]{2,3}')
    uniq_servers = []
    servers = []
    with open(f"/output/http/{host}/aquatone/aquatone_urls.txt", 'r') as f_in:
        servers = f_in.read().splitlines()

    for server in servers:
        uniq_servers.append(p.findall(server)[0][2:])

    for line in open(f"/output/http/{host}/httprobe/httprobe-{host}.txt", "r"):
        fqdn = p.findall(line)[0][2:]
        if fqdn not in uniq_servers: # not a duplicate
            servers.append(line)

    with open(F"/output/http/{host}/webservers-{host}.txt", "w") as f:
        for server in servers:
            f.write(server)

    p = start_proc("wart", host, logger, pool)
    p.get()

    return





