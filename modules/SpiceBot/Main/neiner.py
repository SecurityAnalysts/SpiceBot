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


@sopel.module.commands('neiner', 'neinerneiner')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    instigator = trigger.nick
    target = spicemanip(bot, triggerargsarray, 1)
    osd(bot, trigger.sender, 'action', instigator + " wispers to " + bot.nick)
    if not target:
        osd(bot, trigger.sender, 'action', bot.nick +  " yells neiner neiner at " + instigator)
    elif target == bot.nick:
        osd(bot, trigger.sender, 'action', bot.nick + " slaps " + instigator + " in the face for being a complete and utter moron.")
    else:
        osd(bot, trigger.sender, 'action', bot.nick +  " yells neiner neiner at " + target)
