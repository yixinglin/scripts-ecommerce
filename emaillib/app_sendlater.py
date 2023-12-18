# This web application should be deploy locally
# python app_schedule --mode test
# -a archive.txt -e to_send\ -l info.log --debug True
import sys
sys.path.append(".")
from requests.exceptions import ConnectionError, Timeout
from emaillib.rest.SendLatterRestApi import SendLatterRestApi

import os
from emaillib import *
import logging
from typing import List
from random import random, sample
from common import decode_email_header, nofity_syserr
import traceback
import glo
from glo import conf, conf_path, OS_TYPE
import time 


pth_temp = os.path.join(conf['path'][OS_TYPE]['temp'], conf['env'], 'send-later')
pth_log = os.path.join(conf['path'][OS_TYPE]['cache'], conf['env'], 'log')

class SendLaterApplication: 

    def __init__(self, app: EmailApplication, api:SendLatterRestApi):
        self.app = app
        self.api = api
        self.init()
    
    def init(self):
        conf_path = app.conf_path 
        conf = load_yaml(conf_path)
        c_sendLater = conf['send_later']
        self.eml_folder = os.path.join(pth_temp, 'eml')
        self.history_csv = os.path.join(pth_temp, "history.csv")
        os.makedirs(self.eml_folder, exist_ok=True)

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
                   n_selected_emails_in_round=len(selected_emails_in_round),
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
        is_sent_permitted = self.is_sent_permitted(message['To'])
        is_subscribed = self.is_subscribed(message['To'])
        subject = decode_email_header(message['Subject'])
        if (is_sent_permitted):
            # unsub_link
            message = self.app.send(message, to_addrs) # Send and return the sent message.
            self.update_email_as_sent(message)
            from_addrs, to_addrs = self.get_sender_receiver(message)
            sent += 1
            logging.info(f":Sent from [{from_addrs}] to {to_addrs}")
            # Archive email as sent
            self.append_to_csv("sent", from_addrs, to_addrs, subject, is_subscribed)
            self.app.save_to_mailbox(message)
        else: 
            logging.warning(f":Checked {to_addrs} has been archived or subscription of newsletters was canceled. "
                            f"No emails will be sent to this address currently.")
            from_addrs, to_addrs = self.get_sender_receiver(message)
            self.append_to_csv("rejected", from_addrs, to_addrs, subject, is_subscribed)
        # Delete email file.
        if is_sent_permitted or not is_subscribed:
            # The eml file should be deleted if
            # 1. The email has been sent, or
            # 2. The subscription has been canceled.
            fname = self.remove_email(eml_path)
            logging.info(f":Deleted [{fname}]")
        return sent 
            
    def run(self):
        while(True):
            try:
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
                    else:
                        time.sleep(1)
                self.after_round()
            except (ConnectionError, Timeout) as e:
                logging.error(e)
            time.sleep(self.round_interval)
  

    def update_email_as_sent(self, em: Message): 
        to_ = em['To']
        self.api.update_to_sent(to_)
        return 1

    def remove_email(self, pth) -> str:
        if (os.path.exists(pth)):
            os.remove(pth)
            return pth
        return None 

    def get_registered_email(self, to_addr):
        to_addr = to_addr.strip()
        ls_email = self.api.registered_email(to_addr).content
        ls_email = ls_email['data']
        lem = list(filter(lambda o: o['addr'] == to_addr, ls_email))
        if (len(lem) > 0):
            return lem[0]
        else:
            return None
    def is_sent_permitted(self, to_addr:str):
        lem = self.get_registered_email(to_addr)
        if lem:
            return lem['send_permitted']
        else: # No record in database means sent permitted
            return True

    def is_subscribed(self, to_addr:str):
        lem = self.get_registered_email(to_addr)
        if lem:
            return not lem['unsubscribed']
        else: # No record in database means subscribed
            return True

    def get_sender_receiver(self, message: Message):
        return message['From'], message['To'].split(',')

    def append_to_csv(self, status:str, from_addr:str, to_addrs:List[str], subject:str, subscribed):
        sentAt = current_time(format='%Y-%m-%d,%H:%M:%S')
        to_addrs = "|".join(to_addrs)
        cancel = "subscribed" if subscribed else "canceled"
        with open(self.history_csv, 'a', encoding='utf-8') as fp:
            line = ";".join([status, cancel, sentAt, from_addr, to_addrs, subject])
            fp.write(line + '\n')

if __name__ == '__main__':

    os.makedirs(pth_log, exist_ok=True)
    f_log = os.path.join(pth_log, "email-send-later-app.log")
    setup_logger(f_log, level=conf['log']['level'])
    logging.info(conf)
    debug = not conf['send_later']['actual_send']
    app = EmailApplication(conf_path, debug=debug)  # Email to send newsletter
    api = SendLatterRestApi(conf)
    sl = SendLaterApplication(app, api)

    try:
        # Start the loop
        sl.run()    
    except Exception as e:
        eapp = glo.emailNofity
        nofity_syserr(eapp, eapp.notify_err_emails, "Error: App SendLater", traceback.format_exc())
        logging.error(traceback.format_exc())
        exit(1)
    pass