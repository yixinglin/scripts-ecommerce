import logging
from logging.handlers import TimedRotatingFileHandler
import smtplib
import ssl
from email.header import decode_header
from email.message import Message
from email.mime.text import MIMEText
from email.parser import BytesParser
from typing import List
import yaml


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
                                  TimedRotatingFileHandler(log_file, when='midnight', backupCount=180),
                                  ],
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format="[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] - %(message)s")

def load_yaml(conf_path):
    with open(conf_path, 'r', encoding='utf-8') as f:
        conf = yaml.load(f, Loader=yaml.SafeLoader)
    return conf 

def decode_email_header(item):
    subject, encoding = decode_header(item)[0]
    if encoding==None:
        return subject
    else:
        return subject.decode(encoding)

# ========= Applications ===============
class EmailApplication: 

    def __init__(self, conf_path, debug=True):
        self.conf_path = conf_path
        conf = load_yaml(conf_path)
        conf_smtp = conf['smtp'] 
        self.smtp_host = conf_smtp['host']
        self.smtp_port = conf_smtp['port']  
        self.password = conf_smtp['password']
        self.username = conf_smtp['username']
        self.security = conf_smtp['security']
        self.address = conf_smtp['address']
        self.from_addr = conf_smtp['address']  # Enter your address
        self.to_test_addrs: List[str] = conf_smtp["to_test_addrs"] 
        self.smtp = SmtpEmail(self.smtp_host, self.smtp_port, self.address,
                              self.password, self.security)
        self.debug = debug
        self.notify_err_emails = conf['log']['notification']
        self.notify_admin_emails = conf['server']['admin_contact']
        self.enabled_email_notification = conf['log']['enabled_email_notification']
        self.test_connection()

    def test_connection(self):
        with self.smtp.login() as server:
            print("Connected to SMTP-Server.\n")

    def create_message_from_eml(self, eml_path:str):
        with open(eml_path, 'rb') as f:
            message = BytesParser().parse(f)
        return message
        
    def send(self, message: Message, to_addrs: List[str]) -> Message:
        message = self.smtp.setup_message(self.username, self.from_addr, 
                                to_addrs, message)        
        if not self.debug:
            logging.info(f"INFO: actual send FROM {message['From']} to {message['To']}")
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

    
def nofity_syserr(app:EmailApplication, to_addrs:List[str], subject:str, text:str):
    msg = MIMEText(text)
    msg['From'] = app.from_addr
    msg['To'] = ','.join(to_addrs)
    msg['Subject'] = subject
    app.send(msg, to_addrs)

if __name__ == '__main__':
    addrs = ["abc", "def        ", "qwe ", "rty "]
    unsub = ["d ef ", "qWe           "]
    to_send = customer_list_to_send(addrs, unsub)
    print(to_send)