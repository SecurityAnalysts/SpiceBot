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


@sopel.module.commands('thump', 'thumps')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    instigator = trigger.nick
    target = get_trigger_arg(bot, triggerargsarray, 1)
    reason = get_trigger_arg(bot, triggerargsarray, '2+')
    if not target:
        osd(bot, trigger.sender, 'say', "Did you mean to thump somebody?")
    elif target.lower() not in [u.lower() for u in bot.users]:
        osd(bot, trigger.sender, 'say', "I'm not sure who that is.")
    elif target == bot.nick:
        osd(bot, trigger.sender, 'say', "Well, that's not nice!")
    else:
        if not reason:
            osd(bot, trigger.sender, 'action', 'thumps ' + target + ' on behalf of ' + instigator)
        else:
            osd(bot, trigger.sender, 'action', 'thumps ' + target + ' on behalf of ' + instigator + " because " + reason)
