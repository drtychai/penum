#!/usr/bin/env python3
from flask import Flask
from flask import request
from flask import jsonify
from subprocess import Popen, PIPE
from tool_helper import *

app = Flask(__name__)

@app.route("/")
def index():
    return """Usage:
               Run penum: http://<hostname>[:<port>]/api/<target_host>
               Run specific tool: http://<hostname>[:<port>]/api/<tool>/<target_host>

               Get penum results: http://<hostname>[:<port>]/api/output/<target_host>
               Get specific tool results: http://<hostname>[:<port>]/api/output/<tool>/<target_host>"""

@app.route("/api/<path:host>")
def api(host):
    """Main endpoint to kick of enumeration."""
    ## ToDo: Change the following to utilize multiprocessing
    run_service("amass", host)
    run_service("subfinder", host)
    run_service("aiodnsbrute", host)
    return "penum complete..."

@app.route("/api/amass/<path:host>")
def api_amass(host):
    """Proxy amass service. Returns JSON output."""
    return jsonify(hosts=run_service("amass", host))

@app.route("/api/subfinder/<path:host>")
def api_subfinder(host):
    """Proxy subfinder service. Returns JSON output."""
    return jsonify(hosts=run_service("subfinder", host))

@app.route("/api/aiodnsbrute/<path:host>")
def api_aiodnsbrute(host):
    """Proxy aiodnsbrute service. Reutrns JSON output."""
    return jsonify(hosts=run_service("aiodnsbrute", host))

#####################
# Outputs
#####################
@app.route("/api/output/<path:host>")
def api_output(host):
    """Return JSON of unique list from all tool outputs."""
    tools = ["amass", "subfinder"]
    output = []
    for tool in tools:
       output += get_output(tool, host)
    return jsonify(domain=host, subdomains=list(dict.fromkeys(output)))

@app.route("/api/output/amass/<path:host>")
def api_amass_output(host):
    """Return JSON of amass output."""
    return jsonify(tool="amass", domain=host,
                   subdomains=get_output("amass", host))

@app.route("/api/output/subfinder/<path:host>")
def api_subfinder_output(host):
    """Return JSON of subfinder output."""
    return jsonify(tool="subfinder", domain=host,
                   subdomains=get_output("subfinder", host))

@app.route("/api/output/aiodnsbrute/<path:host>")
def api_aiodnsbrute_output(host):
    """Return JSON of aiodnsbrute output."""
    return jsonify(tool="aiodnsbrute", domain=host,
                   subdomains=get_output("aiodnsbrute", host))

app.run(host="0.0.0.0")
