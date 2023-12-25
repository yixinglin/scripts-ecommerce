import sys
from logging.handlers import TimedRotatingFileHandler

sys.path.append(".")
import glo
import controller
from glo import app
import logging
import os 

OS_TYPE = glo.OS_TYPE

def setup_logger(log_file, level='info'):
    lvd = dict(info=logging.INFO, debug=logging.DEBUG, warning=logging.WARNING, error=logging.ERROR, critical=logging.CRITICAL)
    logging.basicConfig(level=lvd[level],
                        handlers=[ logging.StreamHandler(),
                                  TimedRotatingFileHandler(log_file, when='midnight', backupCount=180, encoding='utf-8'),
                                  ],
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format="[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] - %(message)s")

if __name__ == '__main__':
    conf = glo.conf
    log_dir = os.path.join(conf[OS_TYPE]["cache"], "log")
    os.makedirs(conf[OS_TYPE]["temp"], exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)
    pth_log = os.path.join(log_dir, 'gls.log')
    setup_logger(pth_log, 'info')
    logging.info(conf)
    app.run(host=conf['server']['address'], 
            port=conf['server']['port'], 
            threaded=True, 
            debug=False)
    