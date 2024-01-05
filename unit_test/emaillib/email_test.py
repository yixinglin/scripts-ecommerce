import sys
from email.mime.text import MIMEText
from email.utils import formatdate

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
    del msg['Date']
    msg['Date'] = formatdate(localtime=True)
    eapp.imap.append(msg, flags='')
    # smtplib.SMTPRecipientsRefused
    eapp.send(msg, ["184059914example.com"])

