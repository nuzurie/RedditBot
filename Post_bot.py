import time
import json
import praw
import re

from item_dictionary import update_item_dict

reddit = praw.Reddit(client_id='mF2x9Cn0IdTg0g',
                     client_secret='_qrjkZYbdZ4xCww-CKyu_edUT8I',
                     user_agent='<console:item_bot:0.0.1 (by /u/MZNurie)',
                     username='dota2_itembot',
                     password="")

errors = 0

subreddits = reddit.subreddit("bottest")
hot_reddit = subreddits.hot(limit=20)

with open('item_dict.txt', 'r') as item_dictionary:
    items = json.load(item_dictionary)


def find_item(comment_check):
    if comment_check.body.find('!itembot') != -1:
        item_query = comment_check.body.split(' ')[1].lower()
        if item_query == "update":
            update_item_dict()
        if item_query in items:
            comment_reply = items[item_query]
            comment_check.reply(comment_reply)


def post():
    global errors

    try:
        for submission in hot_reddit:
            if not submission.stickied:
                print('Title: {}, ups: {}, Visited: {}'.format(submission.title,
                                                               submission.ups,
                                                               submission.visited))
                submission.comments.replace_more(limit=0)
                for comment in submission.comments.list():
                    find_item(comment)
                    if len(comment.replies) > 0:
                        for reply in comment.replies:
                            find_item(reply)
    except praw.exceptions.APIException as e:
        if e.error_type == "RATELIMIT":
            delay = re.search("(\d+) minutes?", e.message)

            if delay:
                delay_seconds = float(int(delay.group(1)) * 60)
                time.sleep(delay_seconds)
                post()
            else:
                delay = re.search("(\d+) seconds", e.message)
                delay_seconds = float(delay.group(1))
                time.sleep(delay_seconds)
                post()
    except:
        errors = errors + 1
        if errors > 5:
            exit(1)


post()
