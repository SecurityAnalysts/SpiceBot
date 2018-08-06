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
    if check == 'bot':
        message = "What the " + fuckType + bot.nick
    elif check == 'instigator':
        message = "What the " + fuckType
    elif check == 'valid':
        message = "What the " + fuckType + target
    else:
        reason = target + reason

    if not reason:
        message = message + "!!"
    else:
        message = message + reason + "!!"
    osd(bot, trigger.sender, 'say', message)
