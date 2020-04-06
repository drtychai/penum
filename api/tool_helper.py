#!/usr/bin/env python3
from dns import resolver, reversename
from multiprocessing import Pool
import psql_helper
import socket

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
    logger.info(f"\033[1;34m[+] Starting {tool} on {host}...\033[0m")
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
            logger.info(f"\033[1;32m[*] {tool} FINISHED...\033[0m")
            break
    return

def get_output(tool,host):
    """Return the given tool's output as a list."""
    ret = ''
    try:
        output = b''
        out_f = f"/{tool}-{host}.out"
        with open(out_f, "rb") as f:
            output += f.read()
        ret = str(output, encoding="utf-8").rstrip().split()
        if tool == "nmap":
            # If XML, don't split into list
            ret = str(output, encoding="utf-8").rstrip()
    except FileNotFoundError:
        raise FileNotFoundError
    return ret

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

    logger.info("-"*50)
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
    logger.info(f"\033[1;34m[+] Updating database with subdomains of {host}...\033[0m")
    psql_helper.update_subdomains(f"/output/subdomain/subdomains-{host}.json", logger)
    logger.info(f"\033[1;32m[+] Database update complete...\033[0m")
    return

def http_enum(host, logger):
    """Main controler for HTTP enumeration tools."""
    pool = Pool()
    procs = []
    tools = ["aquatone", "httprobe"]

    logger.info("\033[0;32m[+] Beginning HTTP enumeration...\033[0m")
    for tool in tools:
        p = start_proc(tool, host, logger, pool)
        procs.append(p)

    for proc in procs:
        proc.get()

    return





