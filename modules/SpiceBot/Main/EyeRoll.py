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

# author jimender2


@sopel.module.commands('eyeroll')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'eyeroll')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    instigator = trigger.nick
    inchannel = trigger.sender
    target = spicemanip(bot, triggerargsarray, 1)
    reason = spicemanip(bot, triggerargsarray, '2+')

    # No target specified
    if not target:
        osd(bot, trigger.sender, 'say', "Who/what would you like to roll your eyes at?")

    # Yourself
    elif target == instigator:
        osd(bot, trigger.sender, 'say', "Unless you pop your eyes out of your head you can't roll your eyes at yourself.")

    # spicebot
    elif target == bot.nick:
        osd(bot, trigger.sender, 'say', "Don't even bother. I can't see you")

    # Target is fine
    else:
        if not reason:
            message = instigator + " rolls their eyes at %s." % target
            osd(bot, trigger.sender, 'say', message)
        else:
            message = instigator + " rolls their eyes at %s because %s." % (target, reason)
            osd(bot, trigger.sender, 'say', message)
