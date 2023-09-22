from gls import GLSApi
import yaml 
import os 
import json 

PTH_PAYLOAD = "./gls/payload.json"
PTH_CONF = "./gls/config.yaml"

def loadConfiguration():
    with open(PTH_CONF, "r", encoding="utf-8") as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
    return conf 

def buildAPI(debug=True) -> GLSApi:
    conf = loadConfiguration()
    if (debug):
        api = GLSApi(**conf['gls']['test'])
    else:
        api = GLSApi(**conf['gls']['prod'])
    return api 

def amazonShipment(shipment, api: GLSApi) -> dict:
    parcels = [{"weight": 1, "comment": ""}]
    payload = api.fillForm(shipment["orderNumber"], 
                           shipment["name1"], shipment["name2"], shipment["name3"], 
                           shipment["street"] + " " +shipment["houseNumber"], 
                           shipment["city"], shipment["zip"], 
                           shipment["state"],
                           shipment["country"], "", parcels)
    return payload

def glsLabel(shipment: dict, debug=True) -> dict:
    conf = loadConfiguration()
    api = buildAPI(debug)
    payload = amazonShipment(shipment, api)
    filename = f"{conf['Windows']['temp']}\gls-{payload['references'][0]}{'-TEST' if debug else ''}.json"
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            resp = json.load(f) 
    else:
        resp = api.createParcelLabel(payload)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(resp, f, ensure_ascii=False, indent=3)
    return resp 

if __name__ == '__main__':
    shipment = {
        "country": "de",
        "zip": "56307",
        "state": "Rheinland-Pfalz",
        "city": "Dernbach",
        "street": "Hauptstr.",
        "houseNumber": "60",
        "name1": "Sonja Lenz",
        "name2": None,
        "name3": None,
        "note": "1x FBM Hotgen 39er",
        "orderNumber": "028-7752738-0461157"
    }
    resp = glsLabel(shipment, debug=True)
    print(resp)

    