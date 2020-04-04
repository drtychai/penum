#!/use/bin/env python3
import psycopg2
import json

def query(q):
    """Performs query q on penum DB."""
    conn = None
    try:
        conn = psycopg2.connect(database="penum", user="postgres", password="postgres",
                              host="db", port="5432")
        cur = conn.cursor()
        cur.execute(q)
        conn.commit()

        rows = cur.fetchall()
        return rows
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return

def is_init():
    """Check if output table exists."""
    q = """SELECT EXISTS(
               SELECT * FROM information_schema.tables WHERE table_name='output'
           );"""
    return query(q)[0][0]

def init():
    """Connect to DB and initialize table."""
    print("[+] Initializing database...")
    q = """CREATE TYPE subdomain_type AS (
               fqdn text,
               ipv4 text,
               ipv6 text,
               open_port integer,
               port_service text
           );

           CREATE TABLE output (
               domain text UNIQUE NOT NULL,
               subdomains subdomain_type[],
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
    with open(filename) as f:
        subdomains_json = json.load(f)
    domain = subdomains_json['domain']
    sd_objs = subdomains_json['subdomains'] #array of dicts

    # Check if host has entry. Create one if not.
    q = """SELECT domain FROM output WHERE domain = '%s';""" % domain
    is_empty = not query(q)
    if is_empty:
        q = """INSERT INTO output (domain, last_modified) values ('%s',now());""" % domain
        query(q)

    # Append subdomain_type into array
    q = """UPDATE output SET subdomains = array_cat(subdomains, '{"(%s,%s,%s,%d,%s)"}'), last_modified = now() WHERE domain = '%s';"""
    for sd_obj in sd_objs:
        # skip loop interation if no ip addr
        if sd_obj['status'] == "NXDOMAIN" or 'answers' not in sd_obj['data']:
            continue

        fqdn = sd_obj['name']
        ip_objs = sd_obj['data']['answers']
        for ip_obj in ip_objs:
            ip = ip_obj['data']
            query(q % (fqdn, ip, '::', 443, 'https', domain))
    return


