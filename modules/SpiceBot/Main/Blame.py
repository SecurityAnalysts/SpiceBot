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


@sopel.module.commands('blame')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    instigator = trigger.nick
    whotoblame = get_trigger_arg(bot, triggerargsarray, 1)
    forwhat = get_trigger_arg(bot, triggerargsarray, '2+') or ''
    if not whotoblame:
        botusersarray = get_database_value(bot, bot.nick, 'botusers') or []
        blametargetarray = []
        for u in bot.users:
            if u in botusersarray and u != instigator and u != bot.nick:
                blametargetarray.append(u)
        if blametargetarray == []:
            whotoblame = str(instigator + "'s mom")
        else:
            whotoblame = get_trigger_arg(bot, blametargetarray, 'random')
            osd(bot, trigger.sender, 'say', "It's " + whotoblame + "'s fault.")
    elif whotoblame.lower() not in [u.lower() for u in bot.users]:
        osd(bot, trigger.sender, 'say', "I blame " + whotoblame + " for that.")
    else:
        if not forwhat:
            osd(bot, trigger.sender, 'say', "It's " + whotoblame + "'s fault.")
        elif forwhat.startswith('for'):
            osd(bot, trigger.sender, 'say', "I blame " + whotoblame + " " + str(forwhat) + ".")
        else:
            osd(bot, trigger.sender, 'say', "I blame " + whotoblame + " for " + str(forwhat) + ".")
