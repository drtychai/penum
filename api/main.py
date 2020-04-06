#!/usr/bin/env python3
from flask import Flask
from flask import request
from flask import jsonify
from tool_helper import *
from multiprocessing import Pool, Process
from pytextbelt import Textbelt
import socket
import xmltodict, json
import logging
import time

def init_logger(f_out):
    logger = logging.getLogger('penum')
    if (logger.hasHandlers()):
        logger.handlers.clear()

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    fh = logging.FileHandler(f_out)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    return logger

### Flask

app = Flask(__name__)
@app.route("/")
def index():
    usage="""Usage: curl -X POST -H "Content-Type: application/json"
                         -d '{"Hosts":["<target_host1>","<target_host2>",...,"<target_hostN>"]}' http://<hostname>[:<port>]/api"""
    return usage

@app.route("/", methods=['POST'])
def api():
    """Main endpoint to kick of enumeration."""
    s_time = time.perf_counter()
    logger = init_logger("/logs/flask-api.log")
    try:
        hosts = request.json['Hosts']
        for host in hosts:
            # Subdomain enumeration
            try:
                socket.inet_aton(host)
                find_subdomains(reverseDNS(host), logger)
            except socket.error:
                find_subdomains(host, logger)

            # HTTP enumeration
            http_enum(host, logger)

        # send SMS
        #sms_client = Textbelt.Recipient("<PHONE_NUM>", "<REGION>")
        #sms_client.send("Done.")
        return f"penum started on the following hosts: {hosts}"
    except TypeError:
        raise TypeError("Content-Type header required.")
    finally:
        elapsed = time.perf_counter() - s_time
        logger.info(f"\033[0;34m[+]{__file__} executed in {elapsed:0.2f} seconds.\033[0m")
    return

app.run(host="0.0.0.0")
