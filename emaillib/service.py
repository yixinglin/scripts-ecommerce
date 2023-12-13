import logging 
import os 
import glo
from glo import db 
from flask import g  
import traceback
from dao import T_Email
from pylib.ioutils import base64encode_urlsafe

FILE_UNSUBS = "file_unsubs.txt"
OS_TYPE = glo.OS_TYPE

class NewLetterService:

    def __init__(self) -> None:
        self.conf = glo.getValue('conf')
        self.file_unsubs = os.path.join(self.conf[OS_TYPE]['temp'], FILE_UNSUBS) 
        
    def is_unsubscribed(self, email_addr):
        res =  T_Email.query.filter_by(address=email_addr, unsubscribed=True).count()
        print(res)
        return res > 0


    def save_to_unsubscribed(self, email_addr):
        try:
            em = T_Email(email_addr, None, 0, True)
            instance = T_Email.query.filter_by(address=email_addr).first()
            if instance:
                instance.unsubscribed = True 
            else:
                db.session.add(em)
            db.session.commit()
        except Exception as e:
            traceback.print_exc() 
        pass 

    def unsubscribe(self, email_addr:str):
        if self.is_unsubscribed(email_addr):
            logging.warning(f":unsubscribed: {email_addr} has been unsubscribed before.") 
        else:
            self.save_to_unsubscribed(email_addr)

    def get_list_unsubscribed(self, encode=False):
        res =  T_Email.query.filter_by(unsubscribed=True).all()
        lines = [em.address for em in res ]
        if encode:
            lines = [ base64encode_urlsafe(li) for li in lines ]
        return lines 