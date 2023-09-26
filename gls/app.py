import glo
import controller
glo._init()
from glo import app
import sys 
import logging
import yaml 
from ip_filter import isInWhiteList
import os 
import platform


OS_TYPE = glo.OS_TYPE

def setupLogger():
    conf = glo.getValue("conf")
    PARENT = conf[OS_TYPE]["cache"]
    pth_log = os.path.join(PARENT, conf[OS_TYPE]["cache"], 'gls.log')
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, datefmt  = '%Y-%m-%d %H:%M:%S',
                        format="[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] - %(message)s")
    formatter = logging.Formatter(
        "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d]: %(message)s")
    fileHandler = logging.FileHandler(pth_log, encoding='UTF-8')
    fileHandler.setLevel(logging.INFO) 
    fileHandler.setFormatter(formatter)
    app.logger.addHandler(fileHandler)

def loadConfiguration(path):
    with open(path, "r", encoding="utf-8") as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
    return conf 

if __name__ == '__main__':
    if (len(sys.argv) <= 1):
        print("Please specify the configuration file.")
        exit(1)
    else: 
        PTH_CONF = sys.argv[1]

    conf = loadConfiguration(PTH_CONF)
    os.makedirs(conf[OS_TYPE]["cache"], exist_ok=True)
    os.makedirs(conf[OS_TYPE]["temp"], exist_ok=True)
    glo.setValue("app", app)
    glo.setValue("PTH_CONF", PTH_CONF)
    glo.setValue("conf", conf)
    setupLogger()
    app.run(host=conf['server']['address'], 
            port=conf['server']['port'], 
            threaded=True, 
            debug=False)
    