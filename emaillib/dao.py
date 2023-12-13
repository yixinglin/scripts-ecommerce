from glo import app, db
from sqlalchemy.sql import func


class T_Email(db.Model):
    __tablename__ = "t_email"
    address = db.Column(db.String(80), primary_key=True)
    latestSentAt = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())  
    sentCount = db.Column(db.Integer)
    unsubscribed = db.Column(db.Boolean)

    def __init__(self, address, latestSentAt, sentCount, unsubscribed):
        self.address = address
        self.latestSentAt = latestSentAt
        self.sentCount = sentCount
        self.unsubscribed = unsubscribed