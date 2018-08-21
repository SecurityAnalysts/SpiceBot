#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *
import praw
from prawcore import NotFound
import ConfigParser
from random import randint
import requests
from fake_useragent import UserAgent
from lxml import html

# user agent and header
ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}

# author deathbybandaid
redditurl = "https://www.reddit.com/"

# Creds
config = ConfigParser.ConfigParser()
config.read("/home/spicebot/spicebot.conf")
USERNAME = config.get("reddit", "username")
PASSWORD = config.get("reddit", "password")
CLIENTID = config.get("reddit", "clientid")
SECRET = config.get("reddit", "secret")

reddit = praw.Reddit(client_id=CLIENTID,
                     client_secret=SECRET,
                     user_agent='spicebot:net.example.myredditapp:v1.2.3 (by /u/SpiceBot-dbb)')


@rule(r"""(?:)r/
          (
            (?:\\/ | [^/])+
          )
          """)
@rule(r"""(?:)u/
          (
            (?:\\/ | [^/])+
          )
          """)
@sopel.module.thread(True)
def mainfunctionnobeguine(bot, trigger):
    triggerargsarray = get_trigger_arg(bot, trigger.group(0), 'create')
    execute_main(bot, trigger, triggerargsarray)


def execute_main(bot, trigger, triggerargsarray):

    rclass = class_create('reddit')

    rclass.channel_current = trigger.sender

    rclass.urlinput = get_trigger_arg(bot, triggerargsarray, 1)
    if rclass.urlinput.endswith("/"):
        searchterm = get_trigger_arg(bot, triggerargsarray, 2)
        rclass.urlinput = str(rclass.urlinput + searchterm)
        triggerargsarray.remove(triggerargsarray[0])
        triggerargsarray.remove(triggerargsarray[0])
        triggerargsarray.insert(0, rclass.urlinput)

    urlsplit = rclass.urlinput.split("/", 1)
    rclass.urltype = get_trigger_arg(bot, urlsplit, 1)
    rclass.urlsearch = get_trigger_arg(bot, urlsplit, 2)
    if rclass.urltype == 'r':
        rclass.urltypetxt = 'subreddit'
    elif rclass.urltype == 'u':
        rclass.urltypetxt = 'user'
    else:
        osd(bot, rclass.channel_current, 'say', "An error has occured.")
        return

    triggerargsarray.remove(triggerargsarray[0])

    page = requests.get(redditurl, headers=header)
    tree = html.fromstring(page.content)
    if page.status_code != 200:
        osd(bot, rclass.channel_current, 'say', "Reddit appears to be down right now.")
        return

    # Run the command's function
    command_function_run = str('reddit_' + rclass.urltype.lower() + '(bot, triggerargsarray, rclass)')
    eval(command_function_run)


def reddit_u(bot, triggerargsarray, rclass):

    subcommand_valid = ['check']
    subcommand = get_trigger_arg(bot, [x for x in triggerargsarray if x in subcommand_valid], 1) or 'check'

    userreal = user_exists(rclass.urlsearch)
    if not userreal:
        osd(bot, rclass.channel_current, 'say', rclass.urlsearch + " appears to be an invalid " + rclass.urltypetxt + "!")
        return
    fulluurul = str(redditurl + rclass.urltype + "/" + rclass.urlsearch)
    if subcommand == 'check':
        osd(bot, rclass.channel_current, 'say', [rclass.urlsearch + " appears to be a valid reddit " + rclass.urltypetxt + "!", fulluurul])
        return


def reddit_r(bot, triggerargsarray, rclass):

    subcommand_valid = ['check', 'hot', 'new', 'top', 'random']
    subcommand = get_trigger_arg(bot, [x for x in triggerargsarray if x in subcommand_valid], 1) or 'check'

    subreal = sub_exists(rclass.urlsearch)
    if not subreal:
        osd(bot, rclass.channel_current, 'say', rclass.urlsearch + " appears to be an invalid " + rclass.urltypetxt + "!")
        return
    fullrurul = str(redditurl + rclass.urltype + "/" + rclass.urlsearch)
    subreddit = reddit.subreddit(rclass.urlsearch)
    if subcommand == 'check':
        dispmsg = []
        dispmsg.append("[Reddit " + rclass.urltype + "/" + rclass.urlsearch + "]")
        if subreddit.over18:
            dispmsg.append("<NSFW>")
        dispmsg.append(str(subreddit.public_description))
        dispmsg.append(fullrurul)
        osd(bot, rclass.channel_current, 'say', dispmsg)
        return

    if subcommand == 'new':
        submissions = subreddit.new(limit=1)
    elif subcommand == 'top':
        submissions = subreddit.top(limit=1)
    elif subcommand == 'hot':
        submissions = subreddit.hot(limit=1)
    elif subcommand == 'random':
        submissions = subreddit.hot(limit=500)
    else:
        osd(bot, rclass.channel_current, 'say', "An error has occured.")
        return
    if subcommand == 'random':
        stoppingpoint = randint(0, 499)
        countings = 0
        for submission in submissions:
            if countings == stoppingpoint:
                continue
            countings += 1
    else:
        submission = submissions[0]

    dispmsg = []
    dispmsg.append("[Reddit " + rclass.urltype + "/" + rclass.urlsearch + " " + subcommand + "]")
    if subreddit.over18:
        dispmsg.append("<NSFW>")
    dispmsg.append("{" + str(submission.score) + "}")
    dispmsg.append(submission.title)
    dispmsg.append(submission.url)
    osd(bot, rclass.channel_current, 'say', dispmsg)


def sub_exists(sub):
    exists = True
    try:
        reddit.subreddits.search_by_name(sub, exact=True)
    except NotFound:
        exists = False
    return exists


def user_exists(user):
    exists = True
    try:
        reddit.redditor(user).fullname
    except NotFound:
        exists = False
    return exists
