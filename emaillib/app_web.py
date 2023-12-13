# This web application should be deploy at clould
import sys 
sys.path.append(".")
import glo
from glo import app, conf, conf_path
import logging
import os 
from emaillib import *
import controller

OS_TYPE = glo.OS_TYPE


if __name__ == '__main__':
    print("Start app_web")
    os.makedirs(conf[OS_TYPE]["cache"], exist_ok=True)
    os.makedirs(conf[OS_TYPE]["temp"], exist_ok=True)
    log_pth = conf[OS_TYPE]["cache"]
    setup_logger(os.path.join(log_pth, "email-app.log"), 
                 level=conf['log']['level'])
    logging.info("CONF: " + conf_path)    
    app.run(host=conf['server']['address'], 
            port=conf['server']['port'], 
            threaded=True, 
            debug=False)