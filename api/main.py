#!/usr/bin/env python3
from flask import Flask
from flask import request
from flask import jsonify
from tool_helper import get_output

app = Flask(__name__)

@app.route("/")
def index():
    return "Usage: http://<hostname>[:<port>]/api/<target_host>"

@app.route("/api/<path:host>")
def api(host):
    qs = request.query_string.decode("utf-8")
    if qs:
        host += "?" + qs

    # Start enumeration
    return jsonify(get_output(host))

@app.route("/api/amass/<path:host>")
def api_amass(host):
    output = ''
    with open("/amass{}.out".format(host), "wb") as f:
        output += f.read()
    return jsonify(str(output, encoding="utf-8").rstrip())

app.run(host="0.0.0.0")
