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