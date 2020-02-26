import json
from all_items import neutral_item_array
from item_parse import get_item_detail

item_dictionary = {}


def update_item_dict():
    for i, key in enumerate(neutral_item_array):
        value = (get_item_detail(neutral_item_array[i]))
        item_dictionary[key.lower()] = value

    with open("item_dict.txt", 'w') as item_file:
        json.dump(item_dictionary, item_file)
