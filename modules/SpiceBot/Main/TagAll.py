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


@sopel.module.commands('tagall')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'tagall')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    instigator = trigger.nick
    allUsers = [u.lower() for u in bot.users]
    users = spicemanip(bot, allUsers, 0) or 'spicebot'
    reason = spicemanip(bot, triggerargsarray, '1+')
    if not reason:
        message = instigator + " is tagging everyone. " + users
    else:
        message = instigator + " is tagging everyone because " + reason + ". " + users

    osd(bot, trigger.sender, 'say', message)
