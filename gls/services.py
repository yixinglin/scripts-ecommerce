from gls import GLSApi
import yaml 
import os 
import json 
import platform
import glo


PTH_PAYLOAD = "./gls/payload.json"
PTH_CONF = "./gls/config.yaml"
OS_TYPE = platform.system()

# app = glo.getValue("app")

def loadConfiguration():
    with open(PTH_CONF, "r", encoding="utf-8") as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
    return conf 

def buildAPI(debug=True) -> GLSApi:
    conf = glo.getValue("conf")
    if (debug):
        api = GLSApi(**conf['gls']['test'])
    else:
        api = GLSApi(**conf['gls']['prod'])
    return api 
# Mapping from amazon to gls payload
def amazonShipment(shipment, api: GLSApi) -> dict:
    parcels = [{"weight": 1, "comment": ""}]*int(shipment['pages'].strip())
    payload = api.fillForm(reference=shipment["orderNumber"], 
                           name1 = shipment["name1"], name2 = shipment["name2"], name3=shipment["name3"], 
                           street=shipment["street"] + " " +shipment["houseNumber"], 
                           city=shipment["city"], zipCode=shipment["zip"], 
                           province=shipment["state"],
                           country=shipment["country"], email=shipment['email'], 
                           phone=shipment["phone"], parcels=parcels)
    return payload

# Create GLS label
    # shipment = {
    #     "country": "de",
    #     "zip": "56307",
    #     "state": "Rheinland-Pfalz",
    #     "city": "Dernbach",
    #     "street": "Hauptstr.",
    #     "houseNumber": "60",
    #     "name1": "Sonja Lenz",
    #     "name2": None,
    #     "name3": None,
    #     "note": "1x FBM Hotgen 39er",
    #     "phone": 123456
    #     "email": abc@gmail.com
    #     "pages": 2
    #     "orderNumber": "028-7752738-0461157"
    # }
def glsLabel(shipment: dict, debug=True) -> dict:
    conf = glo.getValue("conf")
    api = buildAPI(debug)
    payload = amazonShipment(shipment, api)
    filename = os.path.join(f"{conf[OS_TYPE]['temp']}", f"gls-{payload['references'][0]}{'-TEST' if debug else ''}.json") 
    if os.path.exists(filename):
        # app.logger.info("[RESTORE]: ", filename)
        with open(filename, 'r', encoding='utf-8') as f:
            resp = json.load(f) 
    else:
        resp = api.createParcelLabel(payload)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(resp, f, ensure_ascii=False, indent=3)
    return resp 
    