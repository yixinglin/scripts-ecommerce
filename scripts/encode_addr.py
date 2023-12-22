import csv

from pylib.ioutils import base64encode_urlsafe


def main(csv_path, domain):
    delimiter = ';'
    newcsv = []
    fieldnames = []
    with open(csv_path, 'r', encoding='utf-8') as fp:
        reader = csv.DictReader(fp, delimiter=delimiter)
        for row in reader:
            b64 = base64encode_urlsafe(row['email'])
            cancel = f"{domain}/newsletter/unsub?em={b64}"
            row['cancel'] = cancel
            fieldnames = row.keys()
            newcsv.append(row)

    newcsv_path = csv_path + ".base64"
    with open(newcsv_path, 'w', encoding='utf-8', newline='') as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(newcsv)

import sys

if __name__ == '__main__':
    # csv_path = r"newsletter\list_test.csv"
    # domain = "http://127.0.0.1"
    csv_path = sys.argv[1]
    domain = sys.argv[2]
    main(csv_path, domain)

