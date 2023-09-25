from gls import GLSApi
import yaml 
import os 
import json 
import platform
import glo

PTH_PAYLOAD = "./gls/payload.json"
OS_TYPE = platform.system()

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
def glsLabel(shipment: dict) -> dict:
    conf = glo.getValue("conf")
    app = glo.getValue("app")
    api = buildAPI()
    payload = amazonShipment(shipment, api)
    filename = os.path.join(f"{conf[OS_TYPE]['temp']}", f"gls-{payload['references'][0]}.json") 
    if os.path.exists(filename):
        app.logger.info("[RESTORE]: " + filename)
        with open(filename, 'r', encoding='utf-8') as f:
            resp = json.load(f) 
    else:
        resp = api.createParcelLabel(payload)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(resp, f, ensure_ascii=False, indent=3)
        pth_csv = os.path.join(conf[OS_TYPE]['temp'], "gls.csv")
        
        cell = [shipment['orderNumber'], shipment['country'], shipment['state'], 
                shipment['zip']+' '+shipment['city'], 
                shipment['street']+' '+shipment['houseNumber'], 
                shipment['name1'], shipment['name2'], shipment['name3'], shipment['phone']]
        line = ";".join(cell)
        with open(pth_csv, 'a', encoding='utf-8') as f:
            f.write(line + '\n')
    return resp 
    
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
