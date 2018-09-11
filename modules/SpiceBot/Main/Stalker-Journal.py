#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel
from sopel import module, tools
import random
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('stalker')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    instigator = trigger.nick
    whotostalk = get_trigger_arg(bot, triggerargsarray, 1)
    if not whotostalk:
        osd(bot, trigger.sender, 'say', instigator + " updates their stalker journal.")
    else:
        botusersarray = get_database_value(bot, bot.nick, 'botusers') or []
        if whotostalk.lower() not in [u.lower() for u in bot.users]:
            osd(bot, trigger.sender, 'say', "I'm not sure who that is.")
        else:
            osd(bot, trigger.sender, 'say', instigator + " updates their stalker journal entry for " + whotostalk + ".")
