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

#These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[%sm"
BOLD_SEQ = "\033[1m"

def formatter_message(message, use_color = True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message

COLORS = {
    'INFO': '1;34', # Light Blue
    'DEBUG': '0;34', # Dark Blue
    'LGREEN': '1;32' # Light Green,
}

class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color = True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        msg = record.msg
        if self.use_color and levelname in COLORS:
            msg_color = COLOR_SEQ % COLORS[levelname] + msg + RESET_SEQ
            record.msg = msg_color
        return logging.Formatter.format(self, record)


# Custom logger class with multiple destinations
class ColoredLogger(logging.Logger):
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    COLOR_FORMAT = formatter_message(FORMAT, True)
    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.DEBUG)

        color_formatter = ColoredFormatter(self.COLOR_FORMAT)

        fh = logging.FileHandler("/logs/flask-api.log")
        fh.setFormatter(color_formatter)

        self.addHandler(fh)
        return


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
    logging.setLoggerClass(ColoredLogger)
    logger = logging.getLogger('penum')
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
        logger.info(f"{RESET_SEQ}\033[{COLORS['LGREEN']}m[+] penum executed in {elapsed:0.2f} seconds.")
    return

app.run(host="0.0.0.0")
