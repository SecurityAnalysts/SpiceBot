#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import os
import sys
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

commandarray = ["add", "remove", "count", "last"]
# add reset and sort list


@sopel.module.commands('yes', 'yep', 'yeahnahyeah')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'yes')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    instigator = trigger.nick
    inchannel = trigger.sender
    databasekey = 'obviousyes'
    command = spicemanip(bot, triggerargsarray, 1)
    inputstring = spicemanip(bot, triggerargsarray, '2+')
    existingarray = get_database_value(bot, bot.nick, databasekey) or []
    if command in commandarray:
        if command == "add":
            if inputstring not in existingarray:
                adjust_database_array(bot, bot.nick, inputstring, databasekey, 'add')
                message = "Added to database."
            else:
                message = "That is already in the database."
        elif command == "remove":
            if inputstring not in existingarray:
                message = "That was not found in the database."
            else:
                adjust_database_array(bot, bot.nick, inputstring, databasekey, 'del')
                message = "Removed from database."
        elif command == "count":
            messagecount = len(existingarray)
            message = "There are currently " + str(messagecount) + " responses in the database for that."
        # elif command == "list":
        #    if inchannel.startswith("#"):
        #        message = "List can only be run in privmsg to avoid flooding."
        #    else:
        #        message = spicemanip(bot, existingarray, "list")
        elif command == "last":
            message = spicemanip(bot, existingarray, "last")
    else:
        message = spicemanip(bot, existingarray, "random") or ''
        if message == '':
            message = "No response found. Have any been added?"
    osd(bot, trigger.sender, 'say', message)
