#!/usr/bin/env python3
from flask import Flask
from flask import request
from flask import jsonify
from tool_helper import *
from multiprocessing import Pool, Process
import socket
import urllib.parse

app = Flask(__name__)

@app.route("/")
def index():
    usage="""Usage:
    Run penum: curl -X POST -d '{"hosts":["<target_host1>","<target_host2>",...,"<target_hostN>"]}' http://<hostname>[:<port>]/api
    Run specific tool: http://<hostname>[:<port>]/api/<tool>/<target_host>

    Get penum results: http://<hostname>[:<port>]/api/output/<target_host>
    Get specific tool results: http://<hostname>[:<port>]/api/output/<tool>/<target_host>
    """
    return usage

@app.route("/api", methods=['POST'])
def api():
    """Main endpoint to kick of enumeration."""
    hosts = request.json['hosts']
    for host in hosts:
        #urllib.parse.unquote(encodedStr)
        # Check for IP addr
        try:
            socket.inet_aton(addr)
            port_scan(host)
            find_subdomains(reverseDNS(host))
        except socket.error:
            find_subdomains(host)
    return f"penum started on the following hosts: {hosts}"

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

@app.route("/api/sublist3r/<path:host>")
def api_sublist3r(host):
    """Proxy sublist3r service. Reutrns JSON output."""
    return jsonify(hosts=run_service("sublist3r", host))

@app.route("/api/gobuster/<path:host>")
def api_gobuster(host):
    """Proxy gobuster service. Reutrns JSON output."""
    return jsonify(hosts=run_service("gobuster", host))

@app.route("/api/massdns/<path:host>")
def api_massdns(host):
    """Proxy massdns service. Reutrns JSON output."""
    return jsonify(hosts=run_service("massdns", host))


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

@app.route("/api/output/sublist3r/<path:host>")
def api_sublist3r_output(host):
    """Return JSON of sublist3r output."""
    return jsonify(tool="sublist3r", domain=host,
                   subdomains=get_output("sublist3r", host))

@app.route("/api/output/gobuster/<path:host>")
def api_gobuster_output(host):
    """Return JSON of gobuster output."""
    return jsonify(tool="gobuster", domain=host,
                   subdomains=get_output("gobuster", host))

@app.route("/api/output/massdns/<path:host>")
def api_massdns_output(host):
    """Return JSON of massdns output."""
    return jsonify(tool="massdns", domain=host,
                   subdomains=get_output("massdns", host))

@app.route("/api/output/nmap", methods=['POST'])
def api_nmap_output():
    """"Return JSON of nmap output."""
    addr = request.json['addr'][0]
    return jsonify(tool="nmap", results=get_output("nmap", addr))



app.run(host="0.0.0.0")
