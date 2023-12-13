import logging 
import os 
import glo

FILE_UNSUBS = "file_unsubs.txt"
OS_TYPE = glo.OS_TYPE

class NewLetterService:

    def __init__(self) -> None:
        self.conf = glo.getValue('conf')
        self.file_unsubs = os.path.join(self.conf[OS_TYPE]['temp'], FILE_UNSUBS) 
        
    def is_unsubscribed(self, email_addr):
        lines = self.get_list_unsubscribe()
        return email_addr in lines

    def save_to_unsubscribed(self, email_addr):
        file_unsubs = self.file_unsubs
        with open(file_unsubs, 'a') as f:
            f.write(email_addr+'\n')

    def unsubscribe(self, email_addr:str):
        if self.is_unsubscribed(email_addr):
            logging.info(f":unsubscribed: {email_addr} has been unsubscribed before.") 
        else:
            self.save_to_unsubscribed(email_addr)
            logging.info(f":unsubscribed: {email_addr}") 

    def get_list_unsubscribe(self):
        logging.info(f":list_unsubscribed") 
        lines = []
        file_unsubs = self.file_unsubs
        if (os.path.exists(file_unsubs)):
            with open(file_unsubs, 'r', encoding="utf-8")  as f:
                lines = [o.strip() for o in f.readlines()]    
        return lines