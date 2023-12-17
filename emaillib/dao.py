from glo import conf, OS_TYPE
from web_init import db
from sqlalchemy.sql import func
from sqlalchemy import DateTime, Column
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import os 
import shutil 

class T_Email(db.Model):
    __tablename__ = "t_email"
    id = Column(db.Integer, primary_key=True, autoincrement=True)
    addr = Column(db.String(80), nullable=False)
    latestSentAt = Column(DateTime(timezone=True), default=datetime.now)  
    sentCount = Column(db.Integer)
    unsubscribed = Column(db.Boolean, nullable=False)
    updateAt = Column(db.DateTime(timezone=True), 
                         server_default=func.now())

    def __init__(self, addr, unsubscribed):
        self.id = None
        self.addr = addr
        self.latestSentAt = datetime.today() -  timedelta(days=365)
        self.sentCount = 0
        self.unsubscribed = unsubscribed
        self.updateAt = datetime.now()

def backup_database():
    pth1 = conf['server'][OS_TYPE]['db']
    saveOn = datetime.today().strftime('%Y%m%d')
    fname = f"{pth1}.{saveOn}"
    shutil.copy(pth1, fname)
    print(fname)

# Create the background scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=backup_database, trigger="interval", seconds=12*3600)
scheduler.start()
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())