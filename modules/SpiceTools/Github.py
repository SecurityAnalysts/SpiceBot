#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import json
import requests
import ConfigParser
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *
from sopel.module import ADMIN


# Creds
config = ConfigParser.ConfigParser()
config.read("/home/spicebot/spicebot.conf")
USERNAME = config.get("github", "username")
PASSWORD = config.get("github", "password")

# Repo
REPO_OWNER = 'SpiceBot'
REPO_NAME = 'SpiceBot'

# Invalid Requests
dontaskforthese = ['instakill', 'instant kill', 'random kill', 'random deaths', 'butterfingers', 'bad grenade', 'grenade failure', 'suicide', 'go off in', 'dud grenade']


@sopel.module.commands('feature', 'feetcher', 'fr', 'bug', 'br', 'borked', 'issue', 'wiki')
def execute_main(bot, trigger):
    banneduserarray = get_database_value(bot, bot.nick, 'users_blocked_github') or []  # Banned Users
    maincommand = trigger.group(1)
    instigator = trigger.nick
    inputtext = trigger.group(2) or 'nothing'
    badquery = 0
    baduser = 0
    noquery = 0
    if maincommand == 'feature' or maincommand == 'feetcher' or maincommand == 'fr':
        labels = ['Feature Request']
        title = 'Feature Request'
        action = " requested"
        assignee = ''
    elif maincommand == 'wiki':
        labels = ['Wiki Update']
        title = 'Wiki Update'
        action = " requested"
        assignee = "Berserkir-Wolf"
    else:
        labels = ['Issue Report']
        title = 'Issue Report'
        action = " found an issue"
        assignee = ''
    if inputtext == 'nothing':
        noquery = 1
    for request in dontaskforthese:
        if request in inputtext and not trigger.admin:
            badquery = 1
    if str(instigator) in banneduserarray:
        baduser = 1
    if badquery or baduser or noquery:
        if badquery:
            if inputtext.startswith('duel'):
                osd(bot, trigger.sender, 'say', "The duels developer has already said no to that. Stop asking.")
            else:
                osd(bot, trigger.sender, 'say', "That feature has already been rejected by the dev team.")
        if baduser:
            osd(bot, trigger.sender, 'say', "Due to abusing this module you have been banned from using it, %s" % instigator)
        if noquery:
            osd(bot, trigger.sender, 'say', "What feature/issue do you want to post?")
    else:
        if inputtext.startswith('duel') or inputtext.startswith('rpg'):
            title = "DUELS/RPG: " + title
            assignee = "deathbybandaid"
            body = inputtext
            body = str(instigator + action + ": " + body)
            make_github_issue(bot, body, labels, title, assignee, instigator)
        elif inputtext.startswith('gamble') or inputtext.startswith('casino'):
            title = "CASINO: " + title
            assignee = "josh-cunning"
            body = inputtext
            body = str(instigator + action + ": " + body)
            make_github_issue(bot, body, labels, title, assignee, instigator)
        else:
            body = inputtext
            body = str(instigator + action + ": " + body)
            make_github_issue(bot, body, labels, title, assignee, instigator)


def make_github_issue(bot, body, labels, title, assignee, instigator):
    url = 'https://api.github.com/repos/%s/%s/issues' % (REPO_OWNER, REPO_NAME)
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    if assignee == '':
        issue = {'title': title,
                 'body': body,
                 'labels': labels}
    else:
        issue = {'title': title,
                 'body': body,
                 'assignee': assignee,
                 'labels': labels}
    r = session.post(url, json.dumps(issue))
    if r.status_code == 201:
        osd(bot, instigator, 'priv', "Successfully created " + title)
    else:
        osd(bot, instigator, 'priv', "Could not create " + title)
        osd(bot, instigator, 'priv', str('Response:' + r.content))
