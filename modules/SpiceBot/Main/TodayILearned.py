#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import datetime
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author jimender2


@sopel.module.commands('til')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'til')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    instigator = trigger.nick
    databasekey = 'todayILearned'
    command = spicemanip(bot, triggerargsarray, 1)
    inputstring = spicemanip(bot, triggerargsarray, '2+')
    existingarray = get_database_value(bot, trigger.nick, databasekey) or []
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
    elif command == "last":
        message = spicemanip(bot, existingarray, "last")
    else:
        message1 = spicemanip(bot, existingarray, "random") or ''
        if message1 == '':
            message = "No response found. Have any been added?"
        else:
            message = "Today I Learned that " + message1 + "!"
    osd(bot, trigger.sender, 'say', message)
