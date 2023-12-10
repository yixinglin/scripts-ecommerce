import smtplib
from email.message import Message
import smtplib, ssl
from typing import List
import logging  

class SmtpEmail: 

    def __init__(self, host, port, address, password, security:str) -> None:
        self.host = host 
        self.port = port
        self.address = address  # Email address
        self.password = password
        self.security = security

    def setup_message(self, username:str, from_addr:str, to_addrs: List[str], message:Message) -> Message:
        self.from_addr = from_addr
        self.to_addrs = to_addrs
        self.username = username 
        if username == None or username == "":
            message.replace_header("From", self.from_addr)
        else:
            message.replace_header("From", f"{self.username} <{self.from_addr}>")
        message.replace_header("To", ", ".join(self.to_addrs))
        return message
 
    def login(self):
        server = None 
        if self.security == "ssl/tls":
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL(self.host, self.port, context=context)
        server.login(self.address, self.password)
        return server

    def send(self, message:Message):
        with self.login() as server:
            server.sendmail(self.from_addr, self.to_addrs, 
                            message.as_string())

def customer_list_to_send(addrs: List[str], unsubscribed: List[str]) -> List[str]:
    addrs = [a.lower().strip() for a in addrs]
    unsubscribed = [u.lower().strip() for u in unsubscribed]
    to_send = []
    for a in addrs:
        if a not in unsubscribed:
            to_send.append(a)
    return to_send

def setup_logger(log_file, level = logging.INFO):
    logging.basicConfig(level=level, 
                        handlers=[logging.StreamHandler(),
                                  logging.FileHandler(log_file, mode='a')],
                        datefmt='%Y-%m-%d,%H:%M:%S',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
if __name__ == '__main__':
    addrs = ["abc", "def        ", "qwe ", "rty "]
    unsub = ["d ef ", "qWe           "]
    to_send = customer_list_to_send(addrs, unsub)
    print(to_send)