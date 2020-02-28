from requests_html import HTMLSession
import re


def arrafy_neutral_item():
    session = HTMLSession()
    page = session.get('https://dota2.gamepedia.com/Force_Boots')
    html = page.html
    parser = html.find('.notanavbox')[0].text

    if "Neutral" in parser:
        neutral_item_list = parser[parser.find("Neutral"):parser.find("Removed")]

    neutral_item_list = neutral_item_list.replace("Neutral", '')
    neutral_item_list = re.sub('Tier .', '', neutral_item_list)
    '''neutral_item_list = neutral_item_list.replace("Tier 1", '')
    neutral_item_list = neutral_item_list.replace("Tier 2", '')
    neutral_item_list = neutral_item_list.replace("Tier 3", '')
    neutral_item_list = neutral_item_list.replace("Tier 4", '')
    neutral_item_list = neutral_item_list.replace("Tier 5", '')'''

    neutral_item_array = neutral_item_list.split("\n")
    neutral_item_array = list(filter(None, neutral_item_array))
    for index, each in enumerate(neutral_item_array):
        neutral_item_array[index] = each.replace(" ", "_")

    return neutral_item_array



