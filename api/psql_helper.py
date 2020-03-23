#!/use/bin/env python3
import psycopg2

def query(q):
    """Performs query q on penum DB."""
    try:
        conn = psycopg2.connect(database="penum", user="postgres",
                              host="127.0.0.1", port="5432")
        cur = conn.cursor()
        cur.execute(q)
        rows = cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return rows


def init():
    """Connect to DB and initialize table."""
    q = """CREATE TABLE IF NOT EXIST output (
               host VARCHAR (50) PRIMARY KEY NOT NULL,
               ip VARCHAR (20) NOT NULL,
               fqdn VARCHAR (50) NOT NULL,
               open-port INT NOT NULL,
               port-service VARCHAR (15) NOT NULL,
               last-modified DATETIME);"""
    query(q)
    return


def update_table(filename):
    """Take data in filename and insert into DB."""
    # Create handlers based on filename input
    # amass JSON handler

    return


