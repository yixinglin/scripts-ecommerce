import json 
import base64 
import services 
if __name__ == '__main__':

    services.glsLabel()
    # with open("data.json", 'r', encoding="utf-8") as f:
    #     label = json.load(f)
    
    # pdf = base64.b64decode(label['labels'][0])
    # with open("labels02.pdf", "wb", ) as f:
    #     f.write(pdf)