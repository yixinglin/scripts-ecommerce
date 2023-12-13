# This web application should be deploy locally
# python app_schedule --mode test
# -a archive.txt -e to_send\ -l info.log --debug True
import sys  
sys.path.append(".")
import argparse
import os  
from emaillib import *
import logging
from typing import List, Dict 
import time 
from random import random, sample

class SendLaterApplication: 

    def __init__(self, app: EmailApplication):
        self.app = app 
        self.init()
    
    def init(self):
        conf_path = app.conf_path 
        conf = load_yaml(conf_path)
        c_sendLater = conf['send_later']
        self.eml_folder = c_sendLater['eml_folder']
        self.arch_folder = c_sendLater['arch_folder'] 
        os.makedirs(self.eml_folder, exist_ok=True)
        os.makedirs(self.arch_folder, exist_ok=True)

        self.max_emails_per_hour = c_sendLater['max_emails_per_hour']
        self.min_emails_per_hour = c_sendLater['min_emails_per_hour']
        assert self.max_emails_per_hour >= self.min_emails_per_hour, "max_emails < min_emails"
        self.delay_noise = c_sendLater['delay_noise']
        self.round_interval = c_sendLater['round_interval']

    def delay_send(self, num_to_send: int):
        # num_to_send: Number of emails to send in total
        if num_to_send < 1 or self.max_emails_per_hour < 1:
            return 1
        delay = (3600-self.round_interval) / num_to_send
        delay = max(0.1, delay) + random()*self.delay_noise
        return delay  

    def before_round(self):
        logging.info(":Before Round...")
        emails_to_send = os.listdir(self.eml_folder)
        emails_to_send = list(filter(lambda o: ".eml" in o, emails_to_send))
        n_emails_in_rest = len(emails_to_send)
        selected_emails_in_round = emails_to_send
        n = self.min_emails_per_hour + random()*(self.max_emails_per_hour - self.min_emails_per_hour)
        n = round(n)
        if (n < len(emails_to_send)):
            selected_emails_in_round = sample(emails_to_send, n)
        
        logging.info(f":{len(selected_emails_in_round)}/{n_emails_in_rest} emails was select in this round.")
        ans = dict(n_emails_in_rest=n_emails_in_rest, 
                   n_selected_emails_in_round = len(selected_emails_in_round),
                   selected_emails_in_round=selected_emails_in_round)
        return ans 
        
    def after_round(self):
        logging.info(":After Round...")

    def in_task(self, eml_path) -> int:
        logging.info(":In Task...")
        sent = 0
        # Sent email
        message = self.app.create_message_from_eml(eml_path)
        self.app.print_message_headers(message)
        _, to_addrs = self.get_sender_receiver(message)
        archived = self.is_archived(message['To'])
        print(archived)
        if (not archived):
            message = self.app.send(message, to_addrs) # Send and return the sent message.
            from_addrs, to_addrs = self.get_sender_receiver(message)
            sent += 1
            logging.info(f":Sent from [{from_addrs}] to {to_addrs}")
            # Archive Email 
            self.archive_email_addr(message)
        else: 
            logging.warning(f":Checked {to_addrs} has been archived. No emails will be sent to this address today.")
        # Delete email file.
        fname = self.remove_email(eml_path)
        logging.info(f":Deleted [{fname}]") 
        return sent 

    def run(self):
        while(True):
            bef = self.before_round()
            selected_emails =  bef['selected_emails_in_round']
            delay_task = self.delay_send(len(selected_emails))
            # It lasts 60 min per round.
            for i, emp in enumerate(selected_emails):
                pth = os.path.join(self.eml_folder, emp)
                sent = self.in_task(pth)    
                if (sent > 0):
                    logging.info(f":Delay {delay_task: .1f} seconds.")
                    time.sleep(delay_task)
            self.after_round() 
            time.sleep(self.round_interval)

    def archive_file_name(self):
        fname = f"archive-{current_date()}.txt"
        pth = os.path.join(self.arch_folder, fname)
        return pth

    def archive_email_addr(self, em: Message): 
        pth = self.archive_file_name()
        to_ = em['To']
        with open(pth, 'a') as f:
            f.write(to_ + "\n")
        return pth 

    def remove_email(self, pth):
        os.remove(pth)
        _, tail = os.path.split(pth)
        return tail 
    
    def is_archived(self, to_addr:str):
        to_addr = to_addr.strip()
        pth = self.archive_file_name()
        if (os.path.exists(pth)):
            with open(pth, 'r') as f: 
                archived = [o.strip() for o in f.readlines()]
        return to_addr in archived

    def get_sender_receiver(self, message: Message):
        return message['From'], message['To'].split(',')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", help="App mode", type=str, default=None)
    args = parser.parse_args() 
    mode = args.mode  
    if mode is not None:
        conf_path = os.path.join("emaillib", f"config-{mode}.yaml")
    else:
        conf_path = os.path.join("emaillib", f"config.yaml")

    conf = load_yaml(conf_path)
    setup_logger(conf['log']['path'], level=conf['log']['level'])
    logging.info(conf)
    debug = not conf['send_later']['actual_send']
    app = EmailApplication(conf_path, debug=debug)
    sl = SendLaterApplication(app)
    sl.run()