#!/usr/bin/env python3
from flask import Flask, render_template, request
import json
import logging
import sys
import os.path

app = Flask(__name__)

logger = logging.getLogger('werkzeug')
handler = logging.FileHandler('access.log')
logger.addHandler(handler)
stream = logging.StreamHandler(sys.stdout)
logger.addHandler(stream)

@app.route("/flask/name/create", methods=["POST"])
def name_create():
    name = request.form["create"]
    with open("data.db", "a") as f:
        f.write(f"{name}\n")
    vals = json.dumps({"delete": name})
    response = f"""
    <tr>
        <td><input readonly type="text" name='{name}' value='{name}'></td>
        <td><span id='clickableAwesomeFont'><i class='fas fa-trash fa-lg' name='{{name}}' hx-post='/flask/name/delete' hx-vals='{vals}' hx-target='closest tr' hx-swap='outerHTML swap:0.5s'></i></span></td>
        <td><i class='fas fa-ellipsis-v'></i></td>
    </tr>
    """
    return response


@app.route("/flask/name/delete", methods=["POST"])
def name_delete():
    name = request.form["delete"]
    print(f"{name} removed")
    with open("data.db", "r") as f:
        lines = f.readlines()
    with open("data.db", "w") as f:
        for line in lines:
            if line.strip("\n") != name:
                f.write(line)
    return ""


@app.route("/flask/name/order", methods=["POST"])
def name_order():
    global data
    order = request.form.keys()
    data = list(order)
    print(data)
    return f"Stages reordered - "


@app.route("/flask")
def index():
    with open("data.db", "r") as f:
        data = [l.strip() for l in f.readlines()]
    print("index:")
    print(data)
    print(json.dumps(data))
    return render_template("index.html", items=data)

if __name__ == "__main__":
    if not os.path.exists("data.db"):
        with open("data.db", "w") as f:
            f.write("John\nJane\nDoe\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
