from email.parser import BytesParser
import os
from pathlib import Path
import sys

def create_message_from_eml(eml_path: str):
    with open(eml_path, 'rb') as f:
        message = BytesParser().parse(f)
    return message

def main(eml_dir):
    cnt = 0
    for fi in os.listdir(eml_dir):
        fpath = Path(os.path.join(eml_dir, fi))
        ext = fpath.suffix
        if ext == ".eml":
            message = create_message_from_eml(fpath)
            to_ = message["To"]
            newpth = os.path.join(eml_dir, f"{to_}.eml")
            print(f"[{cnt}] {to_}")
            cnt += 1
            os.rename(fpath, newpth)


if __name__ == '__main__':
    # r"newsletter\eml"
    eml_dir = sys.argv[1]
    main(eml_dir)
