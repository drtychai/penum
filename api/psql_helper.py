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
    q = """CREATE TABLE output (
               domain text UNIQUE NOT NULL,
               subdomains jsonb,
               last_modified TIMESTAMP NOT NULL
           );"""
    query(q)
    return

def has_initial_entry(host):
    """Boolean function to determine if domain has been enumerated."""
    has_entry = False
    q = """SELECT domain FROM output WHERE domain = '%s';""" % host
    is_empty = not query(q)
    if not is_empty:
        has_entry = True
    return has_entry


def update_subdomains(filename, logger):
    """Take data in filename and insert into DB."""
    with open(filename) as f:
        new_subdomains = json.load(f)
    domain = new_subdomains['domain']

    # Check if host has entry
    q = """SELECT subdomains FROM output WHERE domain = '%s';"""
    saved_subdomains = query(q % domain)
    if saved_subdomains:
        sd_json = saved_subdomains[0][0]
        sd_json['subdomain'].extend(new_subdomains['subdomain'])
    else:
        sd_json = new_subdomains

    if not has_initial_entry(domain):
        q = """INSERT INTO output (domain, last_modified) values ('%s',now());"""
        query(q % domain)

    q = """UPDATE output SET subdomains = '%s', last_modified = now() WHERE domain = '%s';"""
    query(q % (json.dumps(sd_json), domain))

    with open(f"/logs/subdomains-{domain}.json", 'w') as outfile:
        json.dump(sd_json, outfile)

    logger.info(f"\033[1;32m[+] Updated JSON saved to ./api/logs/subdomains-{domain}.json\033[0m")
    return
