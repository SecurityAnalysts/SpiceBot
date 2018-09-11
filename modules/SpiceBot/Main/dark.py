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


@sopel.module.commands('dark')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'dark')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    allUsers = [u.lower() for u in bot.users]
    user = get_trigger_arg(bot, allUsers, "random") or 'spicebot'
    osd(bot, trigger.sender, 'say', "It was a dark an stormy night.")
    osd(bot, trigger.sender, 'say', "But not any stormy night. You were alone in the house when you heard a creak right behind you. You turn around and can't believe your eyes.")
    osd(bot, trigger.sender, 'say', "You turn around and see it is " + user)
