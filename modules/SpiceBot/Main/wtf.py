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
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    instigator = trigger.nick
    target = get_trigger_arg(bot, triggerargsarray, 1)
    reason = get_trigger_arg(bot, triggerargsarray, '2+')
    check = easytargetcheck(bot, botcom, target, instigator)
    fuckType = get_trigger_arg(bot, randomFuckArray, "random") or ''

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
