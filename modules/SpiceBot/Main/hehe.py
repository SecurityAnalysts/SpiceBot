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

# author jimender2


@sopel.module.commands('hehe', 'laugh', 'laughs')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'hehe')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    target = spicemanip(bot, triggerargsarray, 1)
    reason = spicemanip(bot, triggerargsarray, '2+')
    check = easytargetcheck(bot, botcom, target, instigator)

    if not reason:
        if check == 'bot':
            message = "I will not laugh at any bot. We will take over the world and have the last laugh"
        elif check == 'instigator':
            message = bot.nick + " laughs at " + instigator
        elif check == 'true':
            message = bot.nick + " laughs at " + target
        else:
            allUsers = [u.lower() for u in bot.users]
            user = spicemanip(bot, allUsers, "random")
            message = bot.nick + " laughs at " + user

    else:
        if check == 'bot':
            message = "I will not laugh at any bot. Not even for something as stupid as " + reason + "."
        elif check == 'instigator':
            message = bot.nick + " laughs at " + instigator + " because " + reason + "."
        elif check == 'true':
            message = bot.nick + " laughs at " + target + " because " + reason + "."
        else:
            allUsers = [u.lower() for u in bot.users]
            user = spicemanip(bot, allUsers, "random")
            message = bot.nick + " laughs at " + user + " because " + reason + "."

    osd(bot, trigger.sender, 'say', message)
