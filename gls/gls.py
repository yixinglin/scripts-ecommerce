import base64
import requests
import yaml
import json 
from typing import List, Dict
import platform
PTH_PAYLOAD = "./gls/payload.json"
PTH_CONF = "./gls/config.yaml"
OS_TYPE = platform.system()

class GLSApi:

    def __init__(self, url, username, password, shipperId) -> None:
        self.url = url 
        self.shipperId = shipperId
        auth = f"{username}:{password}"
        auth = base64.b64encode(auth.encode()).decode()
        self.headers = {
            "Host": "api.gls-group.eu",
            "Accept-Language": "en",
            "Accept-Encoding": "gzip,deflate",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth}"
        }
          
    def createParcelLabel(self, payload) -> dict:
        postUrl = self.url + "/shipments"
        resp = requests.post(postUrl, headers=self.headers, json=payload) 
        if (resp.status_code == 201):
            return json.loads(resp.text)
        else:
            raise Exception(resp.text)
         

    def fillForm(self, reference, name1, name2, name3, 
                 street, city, zipCode, province, country, email, phone, parcels:List[Dict]):
        with open(PTH_PAYLOAD, "r", encoding="utf-8") as f:  
            payload = json.load(f)
        payload["shipperId"] = self.shipperId
        payload["references"] = [reference]
        payload["addresses"]["delivery"]["name1"] = name1
        payload["addresses"]["delivery"]["name2"] = name2
        payload["addresses"]["delivery"]["name3"] = name3
        payload["addresses"]["delivery"]["street1"] = street
        payload["addresses"]["delivery"]["country"] = country
        payload["addresses"]["delivery"]["province"] = province
        payload["addresses"]["delivery"]["city"] = city
        payload["addresses"]["delivery"]["zipCode"] = zipCode
        payload["addresses"]["delivery"]["email"] = email
        payload["addresses"]["delivery"]["phone"] = phone
        payload["parcels"] = parcels
        return payload 



def demo01():
    with open(PTH_CONF, "r", encoding="utf-8") as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
    api = GLSApi(**conf['gls']['test'])
    parcel = [{
            "weight": 1,
            "comment": "Note 1@Test"
        }, {
            "weight": 1,
            "comment": "Note 1@Test"
        }, {
            "weight": 1,
            "comment": "Note 1@Test"
        }]
    payload = api.fillForm("Test-o22-123456723289", 
                           "Fischer gmbh", "Peter Fischer", None,  
                           "Muster str. 123", "Hamburg", "22312", "Hamburg", "DE", "Note", parcel)
    try:
        filename = f"{conf['Windows']['temp']}\gls-{payload['references'][0]}.json"
        label = api.createParcelLabel(payload)
        with open(filename, 'w', encoding="utf-8") as f:
            json.dump(label, f, ensure_ascii=False, indent=3)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    demo01()
        