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


@sopel.module.commands('welcome')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'welcome')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    command = get_trigger_arg(bot, triggerargsarray, 1)
    instigator = trigger.nick
    if command == "first":
        target = get_trigger_arg(bot, triggerargsarray, 2)
        message = instigator + " welcomes " + target + " to the channel"
    elif command == "major":
        message = instigator + " is really glad to see " + target + " again."
    else:
        target = get_trigger_arg(bot, triggerargsarray, 1)
        if not target:
            allUsers = [u.lower() for u in bot.users]
            target = get_trigger_arg(bot, allUsers, "random")
        message = instigator + " is glad to see " + target + " again."

    osd(bot, trigger.sender, 'say', message)
