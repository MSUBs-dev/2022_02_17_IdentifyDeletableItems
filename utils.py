import chardet
import glob
import time
import csv
import os


def load_csv(path: str, delimiter=',', quotechar='"') -> list:
    out_data = []
    if not os.path.exists(path):
        print(f'{path} not found')
    else:
        try:
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f,
                                    quotechar=quotechar,
                                    delimiter=delimiter,
                                    quoting=csv.QUOTE_ALL,
                                    skipinitialspace=True)
                out_data = list(reader)
        except UnicodeDecodeError:
            try:
                with open(path, 'rb') as rawdata:
                    encoding = chardet.detect(rawdata.read(10000))
                with open(path, newline='', encoding=encoding['encoding']) as f:
                    reader = csv.reader(f,
                                        quotechar=quotechar,
                                        delimiter=delimiter,
                                        quoting=csv.QUOTE_ALL,
                                        skipinitialspace=True)
                    out_data = list(reader)
            except UnicodeDecodeError:
                print(f'Error decoding {path}')
    return out_data


def llist_to_dlist(l_list: list) -> list:
    out_data = []
    headers = l_list.pop(0)
    for sublist in l_list:
        temp_dict = {}
        for index, h in enumerate(headers):
            temp_dict[h] = sublist[index]
        out_data.append(temp_dict)
    return out_data


def dlist_to_dict(dlist: list, key) -> dict:
    out_data = {}
    for item in dlist:
        temp = dict(item)
        k = temp.pop(key)
        out_data[k] = temp
    return out_data


def export_csv(d_list: list, name: str) -> None:
    if name.endswith('.csv'):
        name = name.replace('.csv', '')
    now = time.strftime("_%Y_%m_%d_%H%M%S")
    name = name + now + ".csv"
    with open(name, mode='w+', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(list(d_list[0].keys()))
        for line in d_list:
            writer.writerow(list(line.values()))
