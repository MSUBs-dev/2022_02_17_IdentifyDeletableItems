from utils import llist_to_dlist
from utils import dlist_to_dict
from datetime import datetime
from utils import export_csv
from utils import load_csv
from pprint import pprint


def filter_to_books(i_dict: dict) -> dict:
    """
    Filters dictionary to only items that appear to be textbooks using naming convention
    :param i_dict: item dictionary -- internal id as primary key
    :return: dictionary of filtered results
    """
    out_data = {}
    for k in i_dict:
        nme = i_dict[k]['Name']
        typ = nme.replace(' ', '')
        typ = typ.lower()
        typ = typ.split('-')[-1]
        if typ in ['n', 'u', 'p', 'rs']:
            out_data[k] = i_dict[k]
    return out_data


if __name__ == '__main__':
    items_path = 'in/items.csv'
    all_items = load_csv(items_path)
    all_items = llist_to_dlist(all_items)
    all_items.sort(key=lambda x: int(x['Internal ID']))
    all_items = dlist_to_dict(all_items, 'Internal ID')
    today = datetime.now()
    for key in all_items:
        cdate = all_items[key]['Date Created'].upper()
        all_items[key]['Children'] = set()
        all_items[key]['Age'] = (today - datetime.strptime(
            cdate, '%m/%d/%Y %I:%M %p')).days
        if all_items[key]['Last Tran Date'] or all_items[key]['Total Onhand'] not in ['', '0']:
            all_items[key]['Bad'] = True
        else:
            all_items[key]['Bad'] = False
    for key in all_items:
        parent = all_items[key]['Parent IID']
        if parent:
            all_items[parent]['Children'].add(key)

    print('All Items:', len(all_items))
    to_be_deleted = {}
    for key in all_items:
        age = all_items[key]['Age']
        tdate = all_items[key]['Last Tran Date']
        ttqoh = all_items[key]['Total Onhand']
        chdrn = all_items[key]['Children']
        prent = all_items[key]['Parent IID']
        if not tdate and age > 120 \
                and (not ttqoh or ttqoh == '0') \
                and (not chdrn or not any([all_items[k]['Bad'] for k in chdrn])) \
                and not all_items.get(prent, {}).get('Bad', False):
            to_be_deleted[key] = all_items[key]
    print('Deletable items:', len(to_be_deleted))
    tbd = filter_to_books(to_be_deleted)
    print('Deletable Books:', len(tbd))
    export_csv(tbd, 'out/delete')
    print('Remaining Items:',
          len(all_items) - len(tbd))
