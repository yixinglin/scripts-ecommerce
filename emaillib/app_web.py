# This web application should be deploy at clould
import sys 
sys.path.append(".")
import glo
from glo import conf
from web_init import app
import logging
import os 
from emaillib import *
import controller

OS_TYPE = glo.OS_TYPE


if __name__ == '__main__':
    print("Start app_web")
    os.makedirs(conf['server'][OS_TYPE]["cache"], exist_ok=True)
    os.makedirs(conf['server'][OS_TYPE]["temp"], exist_ok=True)
    os.makedirs(conf['log'][OS_TYPE]['path'], exist_ok=True)
    log_pth = os.path.join(conf['log'][OS_TYPE]['path'], "email-webapp.log")
    setup_logger(log_pth, level=conf['log']['level'])
    logging.info(conf)   
    app.run(host=conf['server']['address'], 
            port=conf['server']['port'], 
            threaded=True, 
            debug=False)