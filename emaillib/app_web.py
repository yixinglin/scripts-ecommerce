# This web application should be deploy at clould
import sys 
sys.path.append(".")
import glo
import controller
glo._init()
from glo import app
import logging
import yaml 
import os 
import platform
import argparse
from emaillib import *

OS_TYPE = glo.OS_TYPE

def setupLogger():
    conf = glo.getValue("conf")
    PARENT = conf[OS_TYPE]["cache"]
    pth_log = os.path.join(PARENT, conf[OS_TYPE]["cache"], 'newsletter.log')
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, datefmt  = '%Y-%m-%d %H:%M:%S',
                        format="[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] - %(message)s")
    formatter = logging.Formatter(
        "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d]: %(message)s")
    fileHandler = logging.FileHandler(pth_log, encoding='UTF-8')
    fileHandler.setLevel(logging.INFO) 
    fileHandler.setFormatter(formatter)
    app.logger.addHandler(fileHandler)

if __name__ == '__main__':
    print("Start app_web")
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", help="App mode", type=str, default=None)
    args = parser.parse_args() 
    mode = args.mode  
    if mode is not None:
        conf_path = os.path.join("emaillib", f"config-{mode}.yaml")
    else:
        conf_path = os.path.join("emaillib", f"config.yaml")

    conf = load_yaml(conf_path)
    glo.setValue("app", app)
    glo.setValue("PTH_CONF", conf_path)
    glo.setValue("conf", conf)
    logging.info("CONF: " + conf_path)
    print(conf)
    os.makedirs(conf[OS_TYPE]["cache"], exist_ok=True)
    os.makedirs(conf[OS_TYPE]["temp"], exist_ok=True)
    setupLogger()
    
    app.run(host=conf['server']['address'], 
            port=conf['server']['port'], 
            threaded=True, 
            debug=False)