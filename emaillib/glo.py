from flask import Flask
from flask_cors import CORS
import platform

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