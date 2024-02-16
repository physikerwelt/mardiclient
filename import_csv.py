import os
import sys

import requests
import csv

from mardiclient import MardiClient

mc = MardiClient(user=os.environ.get('MARDI_USER'), password=os.environ.get('MARDI_PASSWORD'), login_with_bot=True)


def import_csv(url):
    with requests.get(url, stream=True) as r:
        lines = (line.decode('utf-8') for line in r.iter_lines())
        for row in csv.DictReader(lines):
            process_row(row)


def process_row(row):
    try:
        article = mc.item.get(entity_id=row['article'])
        article.add_claim('P223', row['software'])
        article.write()
    except Exception as error:
        print(row, error, file=sys.stderr)


if __name__ == '__main__':
    import_csv(sys.argv[1])
