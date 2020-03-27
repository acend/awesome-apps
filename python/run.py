#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import logging
from flask import Flask

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

random_number = random.randint(0,16777215)
hex_number = str(hex(random_number))[2:]

@app.route("/")
def hello():
    return "<h1 style=color:#%s>Hello python</h1>" \
           "<h2>ID: %s</h2>" % (hex_number, hex_number)

if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)
