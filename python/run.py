#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import logging
import os
from flask import Flask
from flask import render_template

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

random_number = random.randint(0,16777215)
hex_number = str(hex(random_number))[2:]

@app.route("/")
def hello():
    return render_template('index.html', hex_number=hex_number)

@app.route("/pod/")
def pod():
    return os.getenv('HOSTNAME', 'not-set')

@app.route("/health")
def health():
    return "ok"

if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)
