import json
import all_items
from item_parse import get_item_detail

item_dictionary = {}
neutral_item_array = all_items.arrafy_neutral_item()
print(neutral_item_array)


def update_item_dict():
    global neutral_item_array
    for i, key in enumerate(neutral_item_array):
        try:
            item_dictionary[key.lower()] = (get_item_detail(neutral_item_array[i]))
            print(item_dictionary)
        except Exception as e:
            with open("item_dict.txt", 'w') as item_file:
                json.dump(item_dictionary, item_file)

update_item_dict()