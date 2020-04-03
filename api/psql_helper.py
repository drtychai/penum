#!/use/bin/env python3
import psycopg2
import json

def query(q):
    """Performs query q on penum DB."""
    try:
        conn = psycopg2.connect(database="penum", user="postgres", password="postgres",
                              host="db", port="5432")
        cur = conn.cursor()
        cur.execute(q)
        rows = cur.fetchall()
        return rows
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return


def init():
    """Connect to DB and initialize table."""
    q = """CREATE TYPE subdomain_type AS (
               fqdn text,
               ipv4 text,
               ipv6 text,
               open_port integer,
               port_service text
           );

           CREATE TABLE output (
               domain text UNIQUE NOT NULL,
               subdomains subdomain_type[] NOT NULL,
               last_modified TIMESTAMP NOT NULL
           );"""
    query(q)
    return

def is_cached(host):
    """Boolean function to determine if domain has been enumerated."""
    cached = False
    q = "SELECT * from output WHERE domain LIKE '%s'", host
    rows = query(q)
    if len(rows) > 1:
        cached = True
    return cached

def update_subdomains(filename):
    """Take data in filename and insert into DB."""
    q = """INSERT INTO output (domain, subdomains, last_modified) VALUES
           (
               '%s',
               '{"(%s,%s,%s,%s,%s)"}'::subdomain_type[],
               now()
           );"""
    with open(filename,'r') as f:
        subdomains_json = json.loads(f.read())
    domain = subdomains_json['domain']
    sd_objs = subdomains_json['subdomains'] #array of dicts

    for sd_obj in sd_objs:
        # skip loop interation if no ip addr
        if sd_obj['status'] == "NXDOMAIN" or 'answers' not in sd_obj['data']:
            continue

        fqdn = sd_obj['name']
        ip_objs = sd_obj['data']['answers']
        for ip_obj in ip_objs:
            ip = ip_obj['data']
            query(q % (domain, fqdn, ip, '::','443','https'))
    return


