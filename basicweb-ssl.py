#!/usr/bin/env python3
#uses flask because of ssl_context='adhoc' and im lazy

from flask import Flask
from flask import Response
from flask import request
app = Flask(__name__)

@app.route('/')
def index():
    return 'Web App with Python Flask!'


@app.route("/base",methods = ['GET', 'POST'])
def nameget():
    r = '''{}'''
    return Response(r, mimetype='application/json')


@app.route("/form",methods = ['GET', 'POST'])
def rnget():
    print(request.form)
    r = '''{}'''
    return Response(r, mimetype='application/json')


app.run(host='0.0.0.0', port=443, ssl_context='adhoc')
