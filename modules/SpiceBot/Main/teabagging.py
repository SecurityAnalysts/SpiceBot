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


@sopel.module.commands('teabaggin', 'teabagging')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'teabaggin')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    instigator = trigger.nick
    reason = spicemanip(bot, triggerargsarray, 0)

    allUsers = [u.lower() for u in bot.users]
    user = spicemanip(bot, allUsers, "random") or 'DoubleD'

    if not reason:
        message = instigator + " lowers their balls into " + user + "\'s mouth."
    else:
        message = instigator + " lowers their balls into " + user + "\'s mouth because " + reason
    osd(bot, trigger.sender, 'say', message)
