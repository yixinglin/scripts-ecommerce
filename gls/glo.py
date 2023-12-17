from flask import Flask
from flask_cors import CORS
import platform
import argparse 
import os 
import yaml 

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

def loadConfiguration(path):
    with open(path, "r", encoding="utf-8") as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
    return conf 

_init()
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", help="App mode", type=str, default=None)
args = parser.parse_args() 
mode = args.mode  

if mode is not None:
    conf_path = os.path.join("gls", f"config-{mode}.yaml")
else:
    conf_path = os.path.join("gls", f"config.yaml")

conf = loadConfiguration(conf_path)
setValue("app", app)
setValue("PTH_CONF", conf_path)
setValue("conf", conf)