from datetime import datetime

import glo
from common import nofity_syserr
from dao import T_Email
from web_init import db
from pylib.ioutils import base64encode_urlsafe


class NewLetterService:

    def __init__(self) -> None:
        self.conf = glo.getValue('conf')
        self.host = self.conf['server']['host']

    def is_unsubscribed(self, email_addr):
        res = T_Email.query.filter_by(addr=email_addr, unsubscribed=True).count()
        return res > 0

    def save_to_email(self, email_addr, subscribed=False, sentAt=None):
        unsubscribed = not subscribed
        instance = T_Email.query.filter_by(addr=email_addr).first()
        if instance:
            # Update if exists
            instance.unsubscribed = unsubscribed
            instance.updateAt = datetime.now()
        else:
            # Insert if not exists
            instance = T_Email(email_addr, unsubscribed)
            db.session.add(instance)

        if sentAt:
            instance.latestSentAt = datetime.now()
        db.session.commit()

    def save_as_unsubscribed(self, email_addr: str):
        self.save_to_email(email_addr, subscribed=False)
        content = f"{email_addr} hat das Newsletter-Abonnement gekündigt."
        subject = "Kündigung des Newsletter-Abonnements"
        nofity_syserr(glo.emailNofity,
                      glo.emailNofity.notify_admin_emails,
                      subject, content)

    def save_as_subscribed(self, email_addr: str):
        self.save_to_email(email_addr, subscribed=True)

    def save_as_sent(self, email_addr: str):
        if not self.is_unsubscribed(email_addr=email_addr):
            self.save_to_email(email_addr, subscribed=True, sentAt=datetime.now())
        else:
            raise RuntimeError("Your costomer has been unsubscribed your newsletter.")

    def get_list_registered_email(self):
        res = T_Email.query.all()
        lines = []
        freq = 3600 * 24  # Sending frequency
        for em in res:
            encoded = base64encode_urlsafe(em.addr)
            lastSentAt = em.latestSentAt
            send_permitted = (datetime.now() - lastSentAt).total_seconds() > freq  # Time allowed
            send_permitted = send_permitted and not em.unsubscribed  # subscribed
            unsubLink = f"{self.host}/newsletter/unsub?em={encoded}"
            d = dict(addr=em.addr, unsubscribed=em.unsubscribed, updateAt=em.updateAt,
                     lastSentAt=lastSentAt, encoded=encoded, send_permitted=send_permitted,
                     unsubLink=unsubLink)
            lines.append(d)
        return lines

    def get_registered_email(self, addr):
        lines = self.get_list_registered_email()
        selected = list(filter(lambda o: o['addr'] == addr, lines))
        return selected
