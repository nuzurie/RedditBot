import time
import json
import praw
import re
import os

from item_dictionary import update_item_dict

username = os.environ.get('id')
password = os.environ.get('pw')
c_id = os.environ.get('dota_client_id')
c_secret = os.environ.get('dota_client_secret')
print(c_secret)

reddit = praw.Reddit(client_id=c_id,
                     client_secret=c_secret,
                     user_agent='<console:item_bot:0.0.1>',
                     username=username,
                     password=password)

subreddits = reddit.subreddit("dota2")
hot_reddit = subreddits.new(limit=10)

with open('item_dict.txt', 'r') as item_dictionary:
    items = json.load(item_dictionary)
with open('comment_ids.txt', 'r') as comment_ids:
    replied_to = json.load(comment_ids)


def find_item(comment_check):
    global replied_to
    print(comment_check.id, comment_check.body)
    if comment_check.id in replied_to:
        return
    if comment_check.body.find('!itembot') != -1:
        item_query = comment_check.body.split(' ')[1].lower()
        if item_query == "update":
            update_item_dict()
        if item_query in items:
            comment_reply = items[item_query]
            comment_check.reply(comment_reply)
            replied_to.append(comment_check.id)


errors = 0


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
        print("Exception", e.message)
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

with open('comment_ids.txt', 'w') as comment_ids:
    json.dump(replied_to, comment_ids)
