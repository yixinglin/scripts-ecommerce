from fnmatch import fnmatch
from typing import List

def isInWhiteList(ip, whitelist: List[str]):
    for wip in whitelist:
        if fnmatch(ip, wip):
            return True
    return False

if __name__ == '__main__':
    whitelist = [
        "192.168.[0-9]*.[0-9]*",
    ]

    ip = "192.168.8.123"
    print(isInWhiteList(ip, whitelist))

    
            
    

