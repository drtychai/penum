#!/usr/bin/env python3
from recon.core import base
import argparse
import datetime
import os
import sys

def run_altdns(domains):
    """Run altDNS with the given args."""
    for domain in domains:
        altCmd = f"python3 /altdns/altdns"
        subdomains = f"/output/subdomain/recon-ng-{domain}.out"
        permList = f"/altdns/words.txt"
        output = f"/output/subdomain/altdns-{domain}.out"

        # python altdns.py -i subdomainsList -o data_output -w permutationsList -r -s results_output.txt
        print("running alt-dns... please be patient :) results will be displayed in "+output)
        os.system(f"{altCmd} -i {subdomains} -o data_output -w {permList} -r -s {output}")
    return

def install_modules(reconBase, modules):
    """Install required modules via recon-ng marketplace."""
    # Install recon modules
    for module in modules:
        reconBase._do_marketplace_install(module)

    # Install reporting modules
    #reconBase._do_marketplace_install('reporting/csv')
    reconBase._do_marketplace_install('reporting/list')
    return

def run_module(reconBase, module, domain):
    """Run the passed module with options set."""
    try:
        m = reconBase._do_modules_load(module)
        m.options['source'] = domain
        m.do_run(None)
    except Exception as e:
        print(f"[-] Exception hit: {e}")
    return

def run_recon(domains, bf_wordlist, is_altdns_set):
    """Initialize recon-ng base class and run core of script."""
    dot_recon_dir = "/.recon-ng"
    stamp = datetime.datetime.now().strftime('%M:%H-%m_%d_%Y')
    wspace = domains[0]+stamp

    reconb = base.Recon(base.Mode.CLI)
    reconb._mode = base.Mode.CLI
    reconb._init_global_options()
    reconb._init_workspace(wspace)

    module_list = ["recon/domains-hosts/brute_hosts", "recon/domains-hosts/bing_domain_web",
                   "recon/domains-hosts/google_site_web", "recon/domains-hosts/netcraft",
                   "recon/domains-hosts/shodan_hostname", "recon/netblocks-companies/whois_orgs",
                   "recon/hosts-hosts/resolve"]
    install_modules(reconb, module_list)

    for domain in domains:
        for module in module_list:
            run_module(reconb, module, domain)
            # subdomain bruteforcing
            m = reconb._do_modules_load("recon/domains-hosts/brute_hosts")
            if bf_wordlist:
                m.options['wordlist'] = bf_wordlist
            else:
                m.options['wordlist'] = f"{dot_recon_dir}/data/hostnames.txt"
                m.options['source'] = domain
            m.do_run(None)

        # Run reporting modules
        #m = reconb._do_modules_load("reporting/csv")
        #m.options['filename'] = f"/output/recon-ng-{domain}.csv"
        #m.do_run(None)

        m = reconb._do_modules_load("reporting/list")
        m.options['filename'] = f"/output/subdomain/recon-ng-{domain}.out"
        m.options['column'] = "host"
        m.do_run(None)

    if is_altdns_set:
        run_altdns(domains)
    return

def main(argv):
    try:
        domains = argv.domains
        if argv.filename:
            with open(argv.filename, 'r') as f:
                domains += f.read()
    except Exception as e:
        print(f"[-] Exception hit: {e}")

    bf_wordlist = argv.wordlist.name if argv.wordlist else ""
    run_recon(domains, bf_wordlist, argv.runAltDns)
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', dest='runAltDns', action='store_true', help="After recon, run AltDNS? (this requires alt-dns)")
    parser.add_argument("-i", dest="filename", type=argparse.FileType('r'), help="input file of domains (one per line)", default=None)
    parser.add_argument("domains", help="one or more domains", nargs="*", default=None)
    parser.add_argument("-w", dest="wordlist", type=argparse.FileType('r'), help="input file of subdomain wordlist. must be in same directory as this file, or give full path", default=None)
    parser.add_argument("-p", dest="permlist", type=argparse.FileType('r'), help="input file of permutations for alt-dns. if none specified will use default list.", default=None)
    argv = parser.parse_args()

    main(argv)
