from gls import GLSApi
import os 
import json 
import glo
from glo import app 
from datetime import datetime

PTH_PAYLOAD = "./gls/payload.json"
OS_TYPE = glo.OS_TYPE

def buildAPI() -> GLSApi:
    conf = glo.getValue("conf")
    api = GLSApi(**conf['gls'])
    return api 

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
def glsLabel(shipment: dict, addAdditionNote=False) -> dict:
    conf = glo.getValue("conf")
    app = glo.getValue("app")
    api = buildAPI()
    payload = amazonShipment(shipment, api)
    parent = f"{conf[OS_TYPE]['temp']}"
    filename = os.path.join(parent, f"gls-{payload['references'][0]}.json") 
    if os.path.exists(filename):
        app.logger.info("[RESTORE]: " + filename)
        with open(filename, 'r', encoding='utf-8') as f:
            resp = json.load(f) 
        isnew = False
    else:
        note = shipment["note"] if addAdditionNote else ""
        resp = api.createParcelLabel(payload, note)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(resp, f, ensure_ascii=False, indent=3)
            app.logger.info("[SAVED] ORDER TO " + filename)
        pth_csv = os.path.join(conf[OS_TYPE]['temp'], "gls.csv")
        note = note.replace("\n", " | ")
        cell = [datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
                shipment['orderNumber'], shipment['country'], shipment['state'], 
                shipment['zip']+' '+shipment['city'], 
                shipment['street']+' '+shipment['houseNumber'], 
                shipment['name1'], shipment['name2'], shipment['name3'], shipment['phone'], note]
        line = ";".join(cell)
        with open(pth_csv, 'a', encoding='utf-8') as f:
            f.write(line + '\n')
            app.logger.info("[RECORDED] CSV: " + line)
        isnew = True 
    return resp, isnew
    
# Mapping from amazon to gls payload
def amazonShipment(shipment, api: GLSApi) -> dict:
     # note = shipment["note"].strip()
    parcels = [{"weight": 1, "comment": ""}]*int(shipment['pages'].strip())
    payload = api.fillForm(reference=shipment["orderNumber"], 
                           name1 = shipment["name1"], name2 = shipment["name2"], name3=shipment["name3"], 
                           street=shipment["street"] + " " +shipment["houseNumber"], 
                           city=shipment["city"], zipCode=shipment["zip"], 
                           province=shipment["state"],
                           country=shipment["country"], email=shipment['email'], 
                           phone=shipment["phone"], parcels=parcels)
    return payload
