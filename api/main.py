#!/usr/bin/env python3
from flask import Flask
from flask import request
from flask import jsonify
from tool_helper import *
from multiprocessing import Pool, Process
import socket
import xmltodict, json

app = Flask(__name__)

@app.route("/")
def index():
    usage="""Usage:
    Run penum: curl -X POST -d '{"hosts":["<target_host1>","<target_host2>",...,"<target_hostN>"]}' http://<hostname>[:<port>]/api
    Run specific tool: curl -X POST -d '{"hosts":["<target_host1>","<target_host2>",...,"<target_hostN>"]}' http://<hostname>[:<port>]/api/<tool>

    Get penum results: curl -X POST -d '{"hosts":["<target_host1>","<target_host2>",...,"<target_hostN>"]}' http://<hostname>[:<port>]/api/output
    Get specific tool results: curl -X POST -d '{"hosts":["<target_host1>","<target_host2>",...,"<target_hostN>"]}' http://<hostname>[:<port>]/api/output/<tool>
    """
    return usage

@app.route("/api", methods=['POST'])
def api():
    """Main endpoint to kick of enumeration."""
    hosts = request.json['hosts']
    for host in hosts:
        # Check for IP addr
        try:
            socket.inet_aton(host)
            port_scan(host)
            find_subdomains(reverseDNS(host))
        except socket.error:
            find_subdomains(host)
    return f"penum started on the following hosts: {hosts}"

@app.route("/api/<path:tool>", methods=['POST'])
def api_tool(tool):
    """Proxy any tool server. Returns JSON ouput."""
    hosts = request.json['hosts']
    for host in hosts:
        run_service(tool, host)
    return f"{tool} ran on the following hosts: {hosts}"

@app.route("/api/output", methods=['POST'])
def api_output():
    """Return JSON of unique list from all tool outputs."""
    tools = ["amass", "subfinder"]
    hosts = request.json['hosts']
    output = []
    # TODO: Fix this nested silliness
    for host in hosts:
        for tool in tools:
            try:
                output += get_output(tool, host)
            except FileNotFoundError:
                pass
    return jsonify(domain=host, subdomains=list(dict.fromkeys(output)))

@app.route("/api/output/<path:tool>", methods=['POST'])
def api_tool_ouput(tool):
    """Return JSON of given tool output."""
    hosts = request.json['hosts']
    output = []
    for host in hosts:
        try:
            output += get_output(tool, host)
        except FileNotFoundError:
            pass
    return jsonify(subdomains=list(dict.fromkeys(output)))

@app.route("/api/output/nmap", methods=['POST'])
def api_nmap_output():
    """"Return JSON of nmap output."""
    addr = request.json['addr'][0]
    try:
        nmap_dict = xmltodict.parse(get_output("nmap", addr))
        ret = json.dumps(nmap_dict)
    except Exception as e:
        nmap_dict = get_output("nmap", addr)
        ret = jsonify(results=json.dumps(nmap_dict))
    return ret

app.run(host="0.0.0.0")
