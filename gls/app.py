from flask import Flask, render_template, request, abort
from flask_cors import CORS
import json 
import services 
import sys 
import glo
glo._init()
import logging
import traceback
import yaml 
from ip_filter import isInWhiteList
from werkzeug.exceptions import HTTPException
import os 
import platform
OS_TYPE = platform.system()

app = Flask(__name__)
CORS(app, resources=r'/*')

@app.before_request
def block_method():
    ip = request.environ.get('REMOTE_ADDR')
    conf = glo.getValue("conf")
    if (not isInWhiteList(ip,conf['ips']['whitelist'])):
        abort(403, "Your ip is not in the whitelist. Please contact the administrator for registration.")

@app.errorhandler(Exception)
def custom400(error):
    e = traceback.format_exc()
    app.logger.error(e)
    return render_template("500_generic.html", error=e, status_code=500), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Generate a GLS label.
@app.route('/gls/label', methods=['POST'])
def gls_label():
    app.logger.info("Remote: " + request.remote_addr)
    shipment = request.form
    app.logger.info(shipment.to_dict())
    label = services.glsLabel(shipment)
    resp = render_template("parcel_label.html", labels=label['labels'], parcels=label['parcels'])
    return resp 

# Page for an exemplary parcel label.
@app.route('/gls/label', methods=['GET'])
def gls_test_label():
    orderNumber = request.args.get("order")
    filename = os.path.join(f"{conf[OS_TYPE]['temp']}", f"gls-{orderNumber}.json") 
    with open(filename, 'r', encoding='utf-8') as f:
        label = json.load(f)
    return render_template("parcel_label.html", labels=label['labels'], parcels=label['parcels'])

# Page for filling up GLS form.
@app.route('/gls/label/form')
def index():
    conf = glo.getValue("conf")
    return render_template("gls_form.html", host=conf["server"]["host"])

def setupLogger():
    conf = glo.getValue("conf")
    pth_log = os.path.join(conf[OS_TYPE]["cache"], 'gls.log')
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, datefmt  = '%Y-%m-%d %H:%M:%S',
                        format="[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] - %(message)s")
    formatter = logging.Formatter(
        "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d]: %(message)s")
    fileHandler = logging.FileHandler(pth_log, encoding='UTF-8')
    fileHandler.setLevel(logging.INFO) 
    fileHandler.setFormatter(formatter)
    app.logger.addHandler(fileHandler)

def loadConfiguration(path):
    with open(path, "r", encoding="utf-8") as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
    return conf 

if __name__ == '__main__':
    if (len(sys.argv) <= 1):
        print("Please specify the configuration file.")
        exit(1)
    else: 
        PTH_CONF = sys.argv[1]

    conf = loadConfiguration(PTH_CONF)
    glo.setValue("app", app)
    glo.setValue("PTH_CONF", PTH_CONF)
    glo.setValue("conf", conf)
    setupLogger()
    app.run(host=conf['server']['address'], 
            port=conf['server']['port'], 
            threaded=True, 
            debug=False)
    