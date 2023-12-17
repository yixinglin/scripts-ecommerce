from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from glo import setValue, conf, OS_TYPE

app = Flask(__name__)
CORS(app, resources=r'/*')

setValue("app", app)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{conf['server'][OS_TYPE]['db']}"
db = SQLAlchemy(app)