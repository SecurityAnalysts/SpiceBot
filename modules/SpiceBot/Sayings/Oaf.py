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

# author dysonparkes
oldthings = ["BBS Servers", "Rev drives", "Tape storage"]


@sopel.module.commands('oaf', 'old')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'oaf')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    channel = trigger.sender
    instigator = trigger.nick
    oldperson = get_trigger_arg(bot, triggerargsarray, 1)
    thingtheyremember = get_trigger_arg(bot, triggerargsarray, '2+') or get_trigger_arg(bot, oldthings, 'random')
    message = "%s is so old, they remember shit like %s" % (oldperson, thingtheyremember)
    validtarget = targetcheck(bot, oldperson, instigator)
    if not oldperson:
        message = "%s is so old they forgot how to input the fucking thing they remember." % instigator

    else:
        if oldperson == bot.nick:
            message = "Hey, I'm not that fucking old, whippersnapper!"
        elif oldperson not in [u for u in bot.users]:
            oldperson = instigator
            thingtheyremember = get_trigger_arg(bot, triggerargsarray, '1+') or get_trigger_arg(bot, oldthings, 'random')
            message = "%s is so old, they remember shit like %s" % (oldperson, thingtheyremember)

    osd(bot, trigger.sender, 'say', message)
