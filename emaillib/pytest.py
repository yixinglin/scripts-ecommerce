import sys 
sys.path.append(".")
from emaillib.service import *
import glo
glo._init()
import argparse
from emaillib import *

# python .\emaillib\pytest.py -m test
if __name__ == "__main__":
    print("Start app_web test")
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", help="App mode", type=str, default=None)
    args = parser.parse_args() 
    mode = args.mode  
    if mode is not None:
        conf_path = os.path.join("emaillib", f"config-{mode}.yaml")
    else:
        conf_path = os.path.join("emaillib", f"config.yaml")

    conf = load_yaml(conf_path)
    glo.setValue("PTH_CONF", conf_path)
    glo.setValue("conf", conf)


    service = NewLetterService()
    email = "184059914@qq.com"
    print(":is_unsubscribed ", service.is_unsubscribed(email)==True)
    print(":save_to_unsubscribed ", service.save_to_unsubscribed(email))
    print(":unsubscribe ", service.unsubscribe(email))
    print(":get_list_unsubscribe ", service.get_list_registered_email())