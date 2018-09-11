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

spankweapons = ['paddle', 'belt']


@sopel.module.commands("spank", "paddle", "paddlin")
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'spank')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    target = get_trigger_arg(bot, triggerargsarray, 1)
    reason = get_trigger_arg(bot, triggerargsarray, '2+')
    message = "Whoops, something went wrong."
    # Nothing specified
    if not target:
        message = "Thaat's a paddlin'"

    # Can't slap the bot
    elif target == bot.nick:
        message = "I will not do that!!"

    # Target is fine
    else:
        weapon = get_trigger_arg(bot, spankweapons, 'random')
        if not reason:
            message = trigger.nick + " spanks " + target + " with a " + weapon + "."
        else:
            if reason.startswith('for'):
                message = trigger.nick + " spanks " + target + " with a " + weapon + " " + reason + "."
            else:
                message = trigger.nick + " spanks " + target + " with a " + weapon + " " + reason + "."
    osd(bot, trigger.sender, 'say', message)
