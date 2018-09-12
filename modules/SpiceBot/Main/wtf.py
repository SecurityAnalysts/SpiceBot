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

randomFuckArray = ["flying fuck", "frickle frackal", "fuck", "fudgical"]


@sopel.module.commands('wtf', 'whatthefuck')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'wtf')
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
    target = spicemanip(bot, triggerargsarray, 1)
    reason = spicemanip(bot, triggerargsarray, '2+')
    check = easytargetcheck(bot, botcom, target, instigator)
    fuckType = spicemanip(bot, randomFuckArray, "random") or ''

    if not reason:
        if check == 'bot':
            message = "What the " + fuckType + " " + bot.nick
        elif check == 'instigator':
            message = "What the " + fuckType
        elif check == 'valid':
            message = "What the " + fuckType + " " + target
        else:
            if not target:
                message = "What the " + fuckType
            else:
                message = "What the " + fuckType + ". Why are you " + target + reason + "!?!?"

    else:
        reason = ". Why are you " + reason + "!?!?"
        if check == 'bot':
            message = "What the " + fuckType + " " + bot.nick + reason
        elif check == 'instigator':
            message = "What the " + fuckType + reason
        elif check == 'valid':
            message = "What the " + fuckType + " " + target + reason
        else:
            message = "What the " + fuckType + reason

    osd(bot, trigger.sender, 'say', message)
