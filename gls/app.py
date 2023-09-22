from flask import Flask, render_template, request
import yaml 
import json 
import services 

DEBUG = True

app = Flask(__name__)

@app.route('/gls-label', methods=['POST'])
def gls_label():
    shipment = json.loads(request.data)
    label = services.glsLabel(shipment, debug=DEBUG)
    return render_template("parcel_label.html", labels=label['labels'], parcels=label['parcels'])

@app.route('/gls-label', methods=['GET'])
def gls_test_label():
    with open('..\\data\gls-028-7752738-0461157-TEST.json', 'r', encoding='utf-8') as f:
        label = json.load(f)
    return render_template("parcel_label.html", labels=label['labels'], parcels=label['parcels'])

@app.route('/')
def index():
    address = {
        'name': "GLS",
        'street': "Muster str. 11"
    }
    return render_template("index.html", address=address)

if __name__ == '__main__':

    # with open(PTH_CONF, "r", encoding="utf-8") as f:
    #     conf = yaml.load(f, Loader=yaml.FullLoader)
    # api = GLSApi(**conf['gls']['test'])
    # parcel = [{
    #         "weight": 1,
    #         "comment": "Note 1@Test"
    #     }   ]
    # payload = api.fillForm("Test-o22-123456789", 
    #                        "Mueller gmbh", "Lisa Mueller", None,  
    #                        "Muster str. 223", "Hamburg", "22312", "DE", "", parcel)
    app.run(debug=True)