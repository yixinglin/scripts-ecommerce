import json
import logging
import os
import traceback

from flask import render_template, request, abort
from werkzeug.exceptions import HTTPException

import glo
import services
from glo import app
from ip_filter import isInWhiteList

OS_TYPE = glo.OS_TYPE

# Generate a GLS label.
@app.route('/gls/label', methods=['POST'])
def gls_label():
    ip = getUserIp()
    logging.info("REMOTE: " + ip)
    shipment = request.form
    data = json.dumps(shipment.to_dict())
    logging.info(data)
    label, isnew = services.glsLabel(shipment, addAdditionNote=True)
    return render_template("parcel_label.html", labels=label['labels'], parcels=label['parcels'], isnew=isnew)

# Page for an exemplary parcel label.
@app.route('/gls/label', methods=['GET'])
def gls_test_label():
    conf = glo.getValue("conf")
    orderNumber = request.args.get("order")
    filename = os.path.join(f"{conf[OS_TYPE]['temp']}", f"gls-{orderNumber}.json") 
    with open(filename, 'r', encoding='utf-8') as f:
        label = json.load(f)
    return render_template("parcel_label.html", labels=label['labels'], parcels=label['parcels'], isnew=False)

# http://127.0.0.1:5001/scripts?channel=amazon&script=order.js
@app.route('/scripts', methods=['GET'])
def get_script():
    channel = request.args.get("channel")
    script = request.args.get("script")
    filename = os.path.join(channel, script)
    with open(filename, 'r', encoding='utf-8',) as f:
        ans = f.read() 
    return ans 

# Page for filling up GLS form.
@app.route('/gls/label/form')
def index():
    ip = request.access_route[-1]  # First Proxy IP
    print(ip, request.host_url, request.headers['Host'])
    conf = glo.getValue("conf")
    return render_template("gls_form.html", host="http://"+ip)

def getUserIp():
    try:
        ip = request.headers['X-Real-IP'] # Flask + nginx
        # ip = request.remote_addr               # User Ip
    except KeyError as e:
        print(e)
        ip = request.environ.get('REMOTE_ADDR')  # Flask
    return ip

@app.before_request
def block_method():
    ip = getUserIp()
    conf = glo.getValue("conf")
    if (not isInWhiteList(ip, conf['ips']['whitelist'])):
        logging.info(f"[THREAD] Unknown IP {ip} was blocked. [{request.method}] {request.url}")
        abort(403, "Your ip is not in the whitelist. Please contact the administrator for registration.")
    else:
        logging.info(f"[THREAD] IP {ip} was approved. [{request.method}] {request.url}")

@app.errorhandler(Exception)
def custom400(error):
    if isinstance(error, (FileNotFoundError, FileExistsError, HTTPException)):
        e = error
    else:
        e = traceback.format_exc()
    logging.error(e)
    return render_template("500_generic.html", error=e, status_code=500), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404