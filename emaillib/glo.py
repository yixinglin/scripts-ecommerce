from flask import Flask
from flask_cors import CORS
import platform
import argparse 
import os 
from emaillib import *
from flask_sqlalchemy import SQLAlchemy

OS_TYPE = platform.system()
app = Flask(__name__)
CORS(app, resources=r'/*')

print("GLO LOADED")
def _init():
    global _global_dict
    _global_dict = {}

def setValue(key, value):
    _global_dict[key] = value

def getValue(key):
    try:
        return _global_dict[key]
    except KeyError as e :
        print(e)

_init()
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", help="App mode", type=str, default=None)
args = parser.parse_args() 
mode = args.mode  
if mode is not None:
    conf_path = os.path.join("emaillib", f"config-{mode}.yaml")
else:
    conf_path = os.path.join("emaillib", f"config.yaml")

conf = load_yaml(conf_path)
setValue("app", app)
setValue("PTH_CONF", conf_path)
setValue("conf", conf)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{conf[OS_TYPE]['db']}"
db = SQLAlchemy(app)