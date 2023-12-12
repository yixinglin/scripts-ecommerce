from common import customer_list_to_send, setup_logger, EmailApplication
from typing import List
from email.message import Message
import time 
import argparse
import os 
import traceback 
import logging 
import smtplib
from random import random

# ============= BulkApplication ====================
# Send Emails one by one. Email was given by a list
class BulkApplication: 

    def __init__(self, app: EmailApplication, to_addrs: List[str], archive_path:str) -> None:
        self.app = app
        self.to_addrs = to_addrs
        self.archive_path = os.path.abspath(archive_path)
        self.archive_dir = os.path.dirname(self.archive_path)
    
    def remove_emails(self, unsubs: List[str]):
        subs = customer_list_to_send(self.to_addrs, unsubs)
        removed = len(self.to_addrs) - len(subs)
        print(f"> {removed} email were removed from the to-send-list ({len(self.to_addrs)}).")
        self.to_addrs = subs 

    def archive_email_addr(self, em):
        with open(self.archive_path, 'a') as f:
            f.write(em + "\n") 

    def before_bulk_send(self, message):
        # Start testing
        confirmed = input("Do you want to start the email test? [y/n]")
        if (confirmed.lower() == 'y'):
            print("Test Email:")
            self.app.print_message_headers(message)
            self.app.test(message)
            print("Test passed.\n") 
        
        # Save emails to file
        filename = self.archive_dir+"\subs.log"
        print(filename)
        with open(filename, 'w') as f: 
            f.write("\n".join(self.to_addrs))

    def in_bulk_send(self, message, index, to_addrs):
        em = to_addrs[index]
        try:
            msg = self.app.send(message, [em])
            logging.info(f"[{index+1}/{len(to_addrs)}] {msg['From']} => {msg['To']}") 
            # Write to archive file.
            self.archive_email_addr(em)
        except smtplib.SMTPRecipientsRefused as ex: 
            logging.error(f"[{index+1}/{len(to_addrs)}] {em}. SMTPRecipientsRefused.") 
            self.archive_email_addr(em)
        except Exception as ex: 
            logging.error(traceback.format_exc())
        
        time.sleep(1 + random()*5) 

    def after_bulk_send(self, message):
        logging.info("Finish")    

    def run(self, message: Message):
        self.before_bulk_send(message)
        subs = self.to_addrs
        print(f"Ready to send message to the following email addresses: ")
        print(", ".join(subs), end="\n\n")
        print(f"\n({'ENV: DEBUG' if self.app.debug else ''})")
        confirmed = input(f"Are you sure to start the bulk send ({len(subs)})? [y/n]")
        if confirmed.lower() == 'y':  
            # Send email one customer by one customer
            for i, _ in enumerate(subs):
                self.in_bulk_send(message, i, subs)
                if i % 20 == 1:
                    print("Pause 60 seconds...")
                    time.sleep(60)
        self.after_bulk_send(message)
        
    
def load_from_params(to_send_path, unsubs_path, archive_path):
    with open(to_send_path, "r") as f:
        to_addrs = [line.strip() for line in f.readlines()]
    with open(unsubs_path, "r") as f:
        unsubs = [line.strip() for line in f.readlines()]
    if (archive_path is not None and os.path.exists(archive_path)):
        with open(archive_path, "r") as f:
            archive = [line.strip() for line in f.readlines()]
    else:
        archive = [] 
    return to_addrs, unsubs, archive

# app.py -c config-test.yaml -s list_send.txt -u unsubs.txt -a archive.txt -l info.log -e "G:/workspace/python/test/sample.eml" --debug true
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Configuration file in YAML format.", type=str, default=None)
    parser.add_argument("-a", "--archive", help="Archive file", type=str, default=None)
    parser.add_argument("-s", "--to-send", help="File that contains "
                        "a list of email addresses where messages will be sent to.", type=str, default=None)
    parser.add_argument("-e", "--eml", help="Eml file", type=str, default=None)
    parser.add_argument("-u", "--unsubs", help="File that contains email "
                        "addresses of who has unsubscribed the ad", type=str, default=None)
    parser.add_argument("-l", "--log", help="Log file", type=str, default=None)
    parser.add_argument("-d", "--debug", help="Debug mode", type=bool, default=False)
    args = parser.parse_args() 

    eml_path = args.eml
    conf_path = args.config 
    archive_path = args.archive 
    unsubs_path = args.unsubs
    emails_path = args.to_send
    log_path = args.log
    debug = args.debug

    to_addrs, unsubs, archive = load_from_params(args.to_send, args.unsubs, args.archive)
    setup_logger(log_path, level=logging.INFO)

    app = EmailApplication(conf_path, debug=debug)
    message = app.create_message_from_eml(eml_path)  # Ad to send
    bulk = BulkApplication(app, to_addrs, archive_path)   
    bulk.remove_emails(unsubs+archive)   # Remove email unsubscribed the Ad
    bulk.run(message) # Start the bulk send




