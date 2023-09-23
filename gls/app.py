from flask import Flask, render_template, request
from flask_cors import CORS
import json 
import services 

DEBUG = True

app = Flask(__name__)
CORS(app, resources=r'/*')

# Generate a GLS label.
@app.route('/gls/label', methods=['POST'])
def gls_label():
    # shipment = json.loads(request.form)
    shipment = request.form
    print(shipment)
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
    conf = services.loadConfiguration()
    return render_template("gls_form.html", host=conf["server"]["host"])

if __name__ == '__main__':
    conf = services.loadConfiguration()
    app.run(host=conf['server']['address'], 
            port=conf['server']['port'], 
            threaded=True, 
            debug=False)