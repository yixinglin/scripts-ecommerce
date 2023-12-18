# This web application should be deploy at clould
import sys 
sys.path.append(".")
import glo
from glo import conf, OS_TYPE
from web_init import app
import logging
import os 
from emaillib import *
import controller

if __name__ == '__main__':
    print("Start app_web")
    pth_temp = os.path.join(conf['path'][OS_TYPE]['temp'], conf['env'], 'newsletter')
    pth_cache = os.path.join(conf['path'][OS_TYPE]['cache'], conf['env'], 'newsletter')
    pth_log = os.path.join(conf['path'][OS_TYPE]['cache'], conf['env'], 'log')
    f_log = os.path.join(pth_log, 'email-webapp.log')

    os.makedirs(pth_temp, exist_ok=True)
    os.makedirs(pth_cache, exist_ok=True)
    os.makedirs(pth_log, exist_ok=True)
    setup_logger(f_log, level=conf['log']['level'])
    logging.info(conf)
    logging.info([pth_temp, pth_cache, f_log])
    app.run(host=conf['server']['address'], 
            port=conf['server']['port'], 
            threaded=True, 
            debug=False)
