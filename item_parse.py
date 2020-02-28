from requests_html import HTMLSession
import imgkit, imgur_uploader
import subprocess, time

session = HTMLSession()


def get_item_detail(url):
    link = 'https://dota2.gamepedia.com/{}'.format(url)
    page = session.get(link)
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

    # Screenshot of the desired wiki page
    options = {'crop-h': 1000, 'crop-x': 170, 'crop-y': 180}
    imgkit.from_url(link, 'temp_item.jpg', options=options)

    # Upload it to imgur
    result = subprocess.check_output(["imgur-uploader", "./temp_item.jpg"])

    # throttle to avoid ratelimit exception
    print("Sleeping for 1 minutes")
    time.sleep(60)
    print("Waking up.")
    result = result.decode("utf-8")
    index = result.find("https")
    result = result[index:-1]

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

    if active and not passive and bonus:
        return_string = ("""Item: {}  
        * Tier: {}  
        * Active: {}  
        * Bonus: {}""".format(name, array[tier + 1],
                              ' '.join(array[active + 1:bonus]),
                              ', '.join(array[bonus + 1:disassemble - 1])))

    if active != 0 and passive != 0 and bonus != 0:
        return_string = ("""Item: {}
        * Tier: {}
        * Active: {}
        * Passive: {}
        * Bonus: {}""".format(name, array[tier + 1],
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
            * Tier: {}  
            * Active: {}  
            * Passive: {}""".format(name, array[tier + 1],
                                    ' '.join(array[active + 1:passive]),
                                    ' '.join(array[passive + 1: disassemble - 1])))

    if active and not passive and not bonus:
        return_string = ("""Item: {}  
        * Tier: {}  
        * Active: {}""".format(name, array[tier + 1],
                               ' '.join(array[active + 1:disassemble - 1])))

    if active == 0 and passive == 0 and bonus:
        return_string = ("""Item: {}  
        * Tier: {}  
        * Bonus: {}""".format(name, array[tier + 1],
                              ', '.join(array[bonus + 1:disassemble])))

    if not active and passive and bonus:
        return_string = (
            """Item: {}  
            * Tier: {}  
            * Passive: {}  
            * Bonus: {}""".format(name, array[tier + 1],
                                  ' '.join(array[passive + 1: bonus]),
                                  ', '.join(array[bonus + 1:disassemble - 1])))

    if not active and passive and not bonus:
        return_string = ("""Item: {}  
        * Tier: {}  
        * Passive: {}""".format(name, array[tier + 1],
                                ' '.join(array[passive + 1: disassemble])))
    print(return_string)
    return return_string + f"""  
    [ScreenCapture]({result})"""
