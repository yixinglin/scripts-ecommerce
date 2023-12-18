import sys
from email.mime.text import MIMEText

sys.path.append(".")
sys.path.append("./emaillib")
from emaillib import EmailApplication

if __name__ == '__main__':
    conf_path = "emaillib/config-dev.yaml"
    # conf = load_yaml(conf_path)
    eapp = EmailApplication(conf_path, debug=False)


    msg = MIMEText("Test")
    msg['From'] = eapp.from_addr
    msg['To'] = ','.join(eapp.to_test_addrs)
    msg['Subject'] = "TEST IMAP"
    eapp.imap.append(msg, flags='')
    #create_message_from_eml()
    #eapp.send()