from utils import llist_to_dlist
from utils import dlist_to_dict
from datetime import datetime
from utils import load_csv
from pprint import pprint


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
    for key in all_items:
        parent = all_items[key]['Parent IID']
        if parent:
            all_items[parent]['Children'].add(key)

    to_be_deleted = {}
    for key in all_items:
        age = all_items[key]['Age']
        tdate = all_items[key]['Last Tran Date']
        if not tdate and age > 120:
            chdrn = all_items[key]['Children']
            if not chdrn or not any([all_items[k]['Last Tran Date']
                                     for k in chdrn]):
                to_be_deleted[key] = all_items[key]
    print(len(all_items))
    print(len(to_be_deleted))
    print(len(all_items) - len(to_be_deleted))

