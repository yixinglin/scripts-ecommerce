from flask import Flask, render_template, request
from flask_cors import CORS
import json 
import services 
import sys 
import glo
glo._init()
import logging

# logging.basicConfig(filename='log.txt', level=logging.INFO, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
DEBUG = True 

app = Flask(__name__)
CORS(app, resources=r'/*')

# Generate a GLS label.
@app.route('/gls/label', methods=['POST'])
def gls_label():
    app.logger.info("Remote addr: " + request.remote_addr)
    shipment = request.form
    print(shipment.to_dict(), end="\n\n")
    # app.logger.info(shipment.to_dict())
    label = services.glsLabel(shipment, debug=DEBUG)
    resp = render_template("parcel_label.html", labels=label['labels'], parcels=label['parcels'])
    return resp 

# Page for an exemplary parcel label.
@app.route('/gls/label', methods=['GET'])
def gls_test_label():
    orderNumber = request.args.get("order")
    with open(f'..\\data\gls-{orderNumber}.json', 'r', encoding='utf-8') as f:
        label = json.load(f)
    return render_template("parcel_label.html", labels=label['labels'], parcels=label['parcels'])

# Page for filling up GLS form.
@app.route('/gls/label/form')
def index():
    conf = glo.getValue("conf")
    # conf = services.loadConfiguration()
    return render_template("gls_form.html", host=conf["server"]["host"])

if __name__ == '__main__':
    DEBUG = False if (len(sys.argv) > 1 and sys.argv[1]) == "--prod" else True 
    if DEBUG: 
        print("[DEBUG MODE] starting")
    else:
        print("[PROD MODE] starting")

    glo.setValue("app", app)
    conf = services.loadConfiguration()
    glo.setValue("conf", conf)



    formatter = logging.Formatter(
        "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s")
    fileHandler = logging.FileHandler('log.txt', encoding='UTF-8')
    fileHandler.setLevel(logging.INFO) 
    fileHandler.setFormatter(formatter)
    
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    streamHandler.setLevel(logging.INFO)
    app.logger.addHandler(fileHandler)
    # app.logger.addHandler(streamHandler)
    app.run(host=conf['server']['address'], 
            port=conf['server']['port'], 
            threaded=True, 
            debug=False)