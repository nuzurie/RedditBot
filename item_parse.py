from requests_html import HTMLSession

session = HTMLSession()
global name, active, tier, bonus, disassemble


def get_item_detail(url):
    page = session.get('https://dota2.gamepedia.com/{}'.format(url))
    html = page.html
    parser = html.find('.mw-parser-output table')[0].text
    array = (parser.split('\n'))
    for index, string in enumerate(array):

        if index == 0:
            name = string
        if string == "Tier":
            tier = index
        elif string == "Passive":
            passive = index
        elif string == "Active":
            active = index
        elif string == "Bonus":
            bonus = index
        elif string == "Disassemble?":
            disassemble = index

    try:
        active
    except NameError:
        active = 0

    try:
        passive
    except NameError:
        passive = 0

    try:
        bonus
    except NameError:
        bonus = 0

    if active != 0 and passive == 0 and bonus != 0:
        return_string = ("""Item: {}  
        Tier: {}  
        Active: {}  
        Bonus: {}""".format(name, array[tier + 1],
                            ' '.join(array[active + 1:bonus]),
                            ', '.join(array[bonus + 1:disassemble - 1])))

    if active != 0 and passive != 0 and bonus != 0:
        return_string = ("""Item: {}
        Tier: {}
        Active: {}
        Passive: {}
        Bonus: {}""".format(name, array[tier + 1],
                            ' '.join(array[
                                     active + 1:passive]),
                            ' '.join(array[
                                     passive + 1: bonus]),
                            ', '.join(
                                array[
                                bonus + 1:disassemble - 1])))

    if active != 0 and passive != 0 and bonus == 0:
        return_string = (
            """Item: {}  
            Tier: {}  
            Active: {}  
            Passive: {}""".format(name, array[tier + 1],
                                  ' '.join(array[active + 1:passive]),
                                  ' '.join(array[passive + 1: disassemble - 1])))

    if active and not passive and not bonus:
        return_string = ("""Item: {}  
        Tier: {}  
        Active: {}""".format(name, array[tier + 1],
                             ' '.join(array[active + 1:disassemble - 1])))

    if active == 0 and passive == 0 and bonus:
        return_string = ("""Item: {}  
        Tier: {}  
        Bonus: {}""".format(name, array[tier + 1],
                            ', '.join(array[bonus + 1:disassemble])))

    if not active and passive and bonus:
        return_string = (
            """Item: {}  
            Tier: {}  
            Passive: {}  
            Bonus: {}""".format(name, array[tier + 1],
                                ' '.join(array[passive + 1: bonus]),
                                ', '.join(array[bonus + 1:disassemble - 1])))

    if not active and passive and not bonus:
        return_string = ("""Item: {}  
        Tier: {}  
        Passive: {}""".format(name, array[tier + 1],
                              ' '.join(array[passive + 1: disassemble])))
    return return_string
