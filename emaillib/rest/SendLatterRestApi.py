import json
import logging
import time
import requests

from pylib.httputils import RestApiResponse
from pylib.ioutils import base64encode_urlsafe

class SendLatterRestApi:

    def __init__(self, conf) -> None:
        self.conf = conf
        self.baseurl = conf['send_later']['api']
        self.username =  "admin-newsletter "
        self.password = "uFwdsi9"
    def update_to_sent(self, email_addr):
        encoded = base64encode_urlsafe(email_addr)
        url = self.baseurl + f"/sent?em={encoded}"
        logging.info(":POST " + url)
        reg = requests.post(url)
        time.sleep(0.2)
        if reg.status_code == 200:
            return RestApiResponse(reg.text, reg.status_code)
        else:
            raise requests.RequestException("update_to_sent")

    def update_to_unsub(self, email_addr):
        encoded = base64encode_urlsafe(email_addr)
        url = self.baseurl + f"/unsub?em={encoded}"
        logging.info(":GET " + url)
        reg = requests.get(url)
        time.sleep(0.2)
        if reg.status_code == 200:
            return RestApiResponse(reg.text, reg.status_code)
        else:
            raise requests.RequestException("update_to_unsub")

    def update_to_sub(self, email_addr):
        encoded = base64encode_urlsafe(email_addr)
        url = self.baseurl + f"/sub?em={encoded}"
        logging.info(":GET " + url)
        reg = requests.get(url)
        time.sleep(0.2)
        if reg.status_code == 200:
            return RestApiResponse(reg.text, reg.status_code)
        else:
            raise requests.RequestException("update_to_unsub")

    def registered_email(self, email_addr):
        encoded = base64encode_urlsafe(email_addr)
        url = self.baseurl + f"/registered?em={encoded}"
        logging.info(":GET " + url)
        reg = requests.get(url)
        time.sleep(0.2)
        if reg.status_code == 200:
            j = json.loads(reg.text)
            return RestApiResponse(j, reg.status_code)
        else:
            raise requests.RequestException("registered_email")

    def list_registered_emails(self):
        url = self.baseurl + "/registered"
        body = {
            "username": self.username,
            "password": self.password
        }
        logging.info(":POST " + url)
        reg = requests.post(url, json=body)
        time.sleep(0.2)
        if reg.status_code == 200:
            j = json.loads(reg.text)
            return RestApiResponse(j, reg.status_code)
        else:
            raise requests.RequestException("list_registered_emails")