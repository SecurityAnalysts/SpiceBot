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


@sopel.module.commands('goldstar')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    target = get_trigger_arg(bot, triggerargsarray, 1)
    for c in bot.channels:
        channel = c
    if not target:
        osd(bot, trigger.sender, 'say', "Who deserves a gold star?")
    elif target.lower() not in bot.privileges[channel.lower()]:
        osd(bot, trigger.sender, 'say', "I'm not sure who that is.")
    elif target == bot.nick:
        bot.action("blushes",channel)
    elif target == trigger.nick:
        osd(bot, trigger.sender, 'say', "Awww. Why don't you pat yourself on the back while you're at it?")
    else:
        osd(bot, trigger.sender, 'say', trigger.nick + " gives " + target + " a gold star for participation.")
