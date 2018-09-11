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


@sopel.module.commands('shame')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'shame')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    instigator = trigger.nick
    inchannel = trigger.sender

    target = spicemanip(bot, triggerargsarray, 1)
    reason = spicemanip(bot, triggerargsarray, '2+')
    # No target specified
    if not target:
        message = "Who/what would you like to shame?"

    # Cannot shame Spicebot
    elif target == bot.nick:
        if not reason:
            message = "Shame. Shame on " + instigator + " for even thinking of that."
        else:
            message = "Shame. Shame on " + instigator + " for even thinking that " + reason

    # Cannot kill self
    elif target == instigator:
        message = "Even " + instigator + " thinks they are bad. Shame, Shame on you."

    # Target is fine
    else:
        if not reason:
            message = instigator + " thinks " + target + " has been a bad boy."
        else:
            message = instigator + " thinks " + target + " has been a bad boy because " + reason + "."

    osd(bot, trigger.sender, 'say', message)
