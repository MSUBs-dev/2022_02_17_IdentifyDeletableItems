import chardet
import time
import csv
import os


def load_csv(path: str, delimiter=',', quotechar='"') -> list:
    """
    Loads CSV data from a path
    :param path: path of the CSV file
    :param delimiter: type of separator used in CSV
    :param quotechar: type of character used for quoting
    :return: list of lists containing CSV data
    """
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
    """
    Converts list of lists into list of dictionaries
    :param l_list: list of lists
    :return: list of dictionaries
    """
    out_data = []
    headers = l_list.pop(0)
    for sublist in l_list:
        temp_dict = {}
        for index, h in enumerate(headers):
            temp_dict[h] = sublist[index]
        out_data.append(temp_dict)
    return out_data


def dlist_to_dict(dlist: list, key) -> dict:
    """
    Converts list of dictionaries into single dictionary
    :param dlist: list of dictionaries
    :param key: the key from each dict whose value will be the output dictionary key
    :return: consolidated dictionary
    """
    out_data = {}
    for item in dlist:
        temp = dict(item)
        k = temp.pop(key)
        out_data[k] = temp
    return out_data


def export_csv(i_dict: dict, name: str) -> None:
    """
    Exports dictionary to CSV file
    :param i_dict: input dictionary
    :param name: the name of the output file
    :return: None
    """
    if name.endswith('.csv'):
        name = name.replace('.csv', '')
    now = time.strftime("_%Y_%m_%d_%H%M%S")
    name = name + now + ".csv"

    # change empty sets and lists to empty strings
    for key in i_dict:
        for subkey in i_dict[key]:
            val = i_dict[key][subkey]
            if not val:
                i_dict[key][subkey] = ''

    # actually do th eexport
    with open(name, mode='w+', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        first_key = list(i_dict.keys())[0]
        writer.writerow(['Internal ID'] +
                        list(i_dict[first_key].keys()))
        for key in i_dict:
            line = [key] + list(i_dict[key].values())
            writer.writerow(line)
