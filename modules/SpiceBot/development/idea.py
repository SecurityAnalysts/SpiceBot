#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import random
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author jimender2


array = ["jump off a bridge"]


@sopel.module.commands('idea', 'goodidea, =')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'idea')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    command = get_trigger_arg(bot, triggerargsarray, 1)
    inputstring = get_trigger_arg(bot, triggerargsarray, '2+')

    if not command:
        rand = random.randint(1, 2)
        if rand == 1:
            getIdea(bot, trigger, 'good')
        elif rand == 2:
            getIdea(bot, trigger, 'bad')

    elif command == 'good':
        databasekey = 'ideagood'
        if not inputstring:
            getIdea(bot, trigger, databasekey)
        else:
            existingarray = get_database_value(bot, bot.nick, databasekey) or []
            if inputstring not in existingarray:
                adjust_database_array(bot, bot.nick, inputstring, databasekey, 'add')
                message = "I think this is a good idea. Let me remember it."
                osd(bot, trigger.sender, 'say', message)
            else:
                message = "I already thought this was a good idea. Don't make me regret it"
                osd(bot, trigger.sender, 'say', message)
    elif command == 'bad':
        databasekey = 'ideabad'
        if not inputstring:
            getIdea(bot, trigger, databasekey)
        else:
            existingarray = get_database_value(bot, bot.nick, databasekey) or []
            if inputstring not in existingarray:
                adjust_database_array(bot, bot.nick, inputstring, databasekey, 'add')
                message = "I think this is a bad idea. Let me remember it."
                osd(bot, trigger.sender, 'say', message)
            else:
                message = "I already know that this is a bad idea."
                osd(bot, trigger.sender, 'say', message)
    else:
        message = "Is this a good or a bad idea?"
        osd(bot, trigger.sender, 'say', message)


def getIdea(bot, trigger, type):
    ideaType = 'idea' + type
    existingarray = get_database_value(bot, bot.nick, ideaType) or []
    if existingarray == []:
        if ideaType == "good":
            existingarray = "kissing your mommy goodbye"
        elif ideaType == "bad":
            existingarray = "killing your friends"
    idea = get_trigger_arg(bot, existingarray, "random") or ''
    if ideaType == "good":
        message = idea " is a good idea... (prolly)"
    elif ideaType == "bad":
        message = "I'm telling you, " + idea + " is a bad idea"
    osd(bot, trigger.sender, 'say', message)
