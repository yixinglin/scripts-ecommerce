from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from glo import setValue, conf, OS_TYPE
import os
app = Flask(__name__)
CORS(app, resources=r'/*')

setValue("app", app)

pth_db = os.path.join(conf['path'][OS_TYPE]['cache'], conf['env'], "db")
os.makedirs(pth_db, exist_ok=True)
f_db = os.path.join(pth_db,  'newsletter.db')
setValue("f_db", f_db)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{f_db}"
db = SQLAlchemy(app)