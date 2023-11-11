import glo 
import base64
import requests
import json 
from typing import List, Dict
import platform
from pylib.ioutils import *
PTH_PAYLOAD = "./gls/payload.json"
PTH_CONF = "./gls/config.yaml"
OS_TYPE = platform.system()

class GLSApi:
    MAX_NAME_LEN = 37

    def __init__(self, url, username, password, shipperId) -> None:
        self.app = glo.getValue("app")
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
          
    def createParcelLabel(self, payload:dict, addictionText:str="") -> dict:
        postUrl = self.url + "/shipments"
        self.app.logger.info("[GLS REQUEST]: " + postUrl)
        resp = requests.post(postUrl, headers=self.headers, json=payload) 
        if (resp.status_code == 201):
            parcel = json.loads(resp.text)
            parcelWithWatermark = self.addTextToParcel(parcel['labels'][0], addictionText)
            parcel['labels'][0] = parcelWithWatermark
            return parcel 
        else:
            raise Exception(f"[GLS] Exception {resp.status_code}.\n{resp.text}")
    
    def addTextToParcel(self, b64Parcel:str, text:str):
        pagesize = getPdfPageSize(b64Parcel) # Pagesize of the parcel
        b64Watermark = createPdfWatermark(text, pagesize=pagesize,
                                    textPosition=(10*mm, 75*mm),
                                    textColor=(1, 0, 0, 0.9),
                                    fontSize=7)
        b64out = addWatermarkToPdf(b64Parcel, b64Watermark)
        return b64out


    def fillForm(self, reference, name1, name2, name3, 
                 street, city, zipCode, province, country, email, phone, parcels:List[Dict]):
        name1, name2, name3 = self.adjustNameFields(name1, name2, name3)
        passed = self.checkNameLength([name1, name2, name3])
        if(not passed):
            raise Exception("Names are too long.")

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

    def checkNameLength(self, names: List[str]):
        for name in names:
            if len(name) > self.MAX_NAME_LEN:
                return False
        return True 

    def adjustNameFields(self, name1, name2, name3):
        tmp = ""
        if (len(name1) >= self.MAX_NAME_LEN):
            tmp = name1[self.MAX_NAME_LEN:]
            name1 = name1[:self.MAX_NAME_LEN]
            if (len(name3) > 0):
                name2 = tmp + " || " +name2
            else:
                name3 = name2
                name2 = tmp
        if (len(name2) >= self.MAX_NAME_LEN):
            tmp = name2[self.MAX_NAME_LEN:]
            name2 = name2[:self.MAX_NAME_LEN]
            if(len(name3) > 0):
                name3 = tmp + " || " + name3 
            else:
                name3 = tmp
        return [name1, name2, name3]
            
