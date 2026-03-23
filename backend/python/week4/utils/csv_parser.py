import csv
from io import TextIOWrapper

def parse_csv(file):
    reader= csv.DictReader(TextIOWrapper(file, encoding='utf-8'))
    data = []

    for row in reader:
        data.append(row)

    return data
