#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

databasekey = 'comcast'

# author jimender2


@sopel.module.commands('comcast')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'comcast')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    instigator = trigger.nick
    inchannel = trigger.sender

    command = get_trigger_arg(bot, triggerargsarray, 1)
    inputstring = get_trigger_arg(bot, triggerargsarray, '2+')
    existingarray = get_database_value(bot, bot.nick, databasekey) or []
    if command == "add":
        if inputstring not in existingarray:
            adjust_database_array(bot, bot.nick, inputstring, databasekey, 'add')
            message = "Added to database."
            bot.say(message)
        else:
            message = "That response is already in the database."
            bot.say(message)
    elif command == "remove":
        if inputstring not in existingarray:
            message = "That response was not found in the database."
            bot.say(message)
        else:
            adjust_database_array(bot, bot.nick, inputstring, databasekey, 'del')
            message = "Removed from database."
            bot.say(message)
    elif command == "count":
        messagecount = len(existingarray)
        message = "There are currently " + str(messagecount) + " responses for that in the database."
        bot.say(message)
    elif command == "last":
        message = get_trigger_arg(bot, existingarray, "last")
        bot.say(message)

    else:
        weapontype = get_trigger_arg(bot, existingarray, "random") or ''
        if weapontype == '':
            message = "No response found. Have any been added?"
            target = get_trigger_arg(bot, triggerargsarray, 1)
            reason = get_trigger_arg(bot, triggerargsarray, '2+')
            msg = "a " + weapontype

    # No target specified
    if not target:
        bot.say(msg)


def get_database_value(bot, nick, databasekey):
    databasecolumn = str(databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value
