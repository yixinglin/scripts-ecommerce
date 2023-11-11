from flask import Flask, render_template, request, abort
import services 
import glo 
from glo import app
import json 
import services 
import traceback
from ip_filter import isInWhiteList
from werkzeug.exceptions import HTTPException

import os 

OS_TYPE = glo.OS_TYPE

# Generate a GLS label.
@app.route('/gls/label', methods=['POST'])
def gls_label():
    app.logger.info("REMOTE: " + request.remote_addr)
    shipment = request.form
    app.logger.info(shipment.to_dict())
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
    print(request.remote_addr, request.host_url)
    conf = glo.getValue("conf")
    return render_template("gls_form.html", host="http://"+request.host)

@app.before_request
def block_method():
    ip = request.environ.get('REMOTE_ADDR')
    conf = glo.getValue("conf")
    if (not isInWhiteList(ip, conf['ips']['whitelist'])):
        app.logger.info(f"[THREAD] Unknown IP {ip} was blocked. [{request.method}] {request.url}")
        abort(403, "Your ip is not in the whitelist. Please contact the administrator for registration.")

@app.errorhandler(Exception)
def custom400(error):
    if isinstance(error, (FileNotFoundError, FileExistsError, HTTPException)):
        e = error
    else:
        e = traceback.format_exc()
    app.logger.error(e)
    return render_template("500_generic.html", error=e, status_code=500), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404