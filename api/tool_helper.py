#!/usr/bin/env python3
from dns import resolver, reversename
from multiprocessing import Pool
import psql_helper
import socket
import logging

def tool_port_map(tool):
    mapping = {"amass":30000,
               "subfinder":30001,
               "aiodnsbrute":30002,
               "sublist3r":30003,
               "gobuster":30004,
               "massdns":30005,
               "recon-ng":30006,
               "aquatone":30007,
               "nmap":30008}
    return mapping[f"{tool}"]

def start_proc(tool, host, logger, pool):
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
        psql_helper.update_table(out_f)
    except FileNotFoundError:
        raise FileNotFoundError
    return ret

def check_cache(host):
    """Checks if host has already been enumerated. Return boolean."""
    result = False
    # TODO: check if file names exists
    return result

def reverseDNS(addr):
    qname = reversename.from_address(addr)
    return str(resolver.query(qname, 'PTR')[0])[:-1]

def find_subdomains(host):
    """Main controller for subdomain enumeration tools."""
    logger = logging.getLogger('penum')
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    fh = logging.FileHandler('/logs/flask-api.log')
    fh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    pool = Pool()
    procs = []
    tools = ["subfinder", "sublist3r",
             "aiodnsbrute", "gobuster",
             "recon-ng"]

    for tool in tools:
        logger.info(f"\033[1;34m[+] Starting {tool}...\033[0m")
        p = start_proc(tool, host, logger, pool)
        procs.append(p)

    # wait until all pool processes complete
    for proc in procs:
        proc.get()

    # amass ingests outputs from other subdomain tools
    logger.info(f"\033[1;34m[+] Starting amass...\033[0m")
    p = start_proc("amass", host, logger, pool)
    p.get()

    # update db with amass output
    #psql_helper.update_table("/output/subdomain/amass.json")
    return

def port_scan(host):
    """"Main controller for IP / Network enumeration."""
    pool = Pool()
    start_proc("nmap", host, None, pool)
    return
