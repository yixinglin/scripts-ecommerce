import smtplib, ssl
from email.message import Message
from email.parser import BytesParser
import yaml 
from typing import List
import logging  
import datetime

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
# ========= Utils =================
def customer_list_to_send(addrs: List[str], unsubscribed: List[str]) -> List[str]:
    addrs = [a.lower().strip() for a in addrs]
    unsubscribed = [u.lower().strip() for u in unsubscribed]
    to_send = []
    for a in addrs:
        if a not in unsubscribed:
            to_send.append(a)
    return to_send

def setup_logger(log_file, level='info'):
    lvd = dict(info=logging.INFO, debug=logging.DEBUG, warning=logging.WARNING, error=logging.ERROR, critical=logging.CRITICAL)
    logging.basicConfig(level=lvd[level], 
                        handlers=[logging.StreamHandler(),
                                  logging.FileHandler(log_file, mode='a')],
                        datefmt='%Y-%m-%d,%H:%M:%S',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def load_yaml(conf_path):
    with open(conf_path, 'r', encoding='utf-8') as f:
        conf = yaml.load(f, Loader=yaml.SafeLoader)
    return conf 

def current_date(format=r"%Y%m%d"):
    return datetime.datetime.today().strftime(format)

# ========= Applications ===============
class EmailApplication: 

    def __init__(self, conf_path, debug=True):
        self.conf_path = conf_path
        conf = load_yaml(conf_path)['smtp']
        self.smtp_host = conf['host']
        self.smtp_port = conf['port']  
        self.password = conf['password']
        self.username = conf['username']
        self.security = conf['security']
        self.address = conf['address']
        self.from_addr = conf['address']  # Enter your address
        self.to_test_addrs: List[str] = conf["to_test_addrs"] 
        self.smtp = SmtpEmail(self.smtp_host, self.smtp_port, self.address,
                              self.password, self.security)
        self.debug = debug
        self.test_connection()

    def test_connection(self):
        with self.smtp.login() as server:
            print("Connected to server.\n")

    def create_message_from_eml(self, eml_path:str):
        with open(eml_path, 'rb') as f:
            message = BytesParser().parse(f)
        return message
        
    def send(self, message: Message, to_addrs: List[str]) -> Message:
        message = self.smtp.setup_message(self.username, self.from_addr, 
                                to_addrs, message)        
        if not self.debug:
            self.smtp.send(message) 
        else:
            logging.debug(f"DEBUG: FROM {message['From']} to {message['To']}")
        return message
    
    def test(self, message: Message):
        self.send(message, self.to_test_addrs) 

    def print_message_headers(self, message):
        print("============= Message Headers ============")
        for item in message.items(): print(f"{item[0]}: {item[1]}")
        print("------------------------------------")

if __name__ == '__main__':
    addrs = ["abc", "def        ", "qwe ", "rty "]
    unsub = ["d ef ", "qWe           "]
    to_send = customer_list_to_send(addrs, unsub)
    print(to_send)