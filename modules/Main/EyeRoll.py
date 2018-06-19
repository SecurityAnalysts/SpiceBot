#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import os
import sys
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

#author jimender2

@sopel.module.commands('eyeroll')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'eyeroll')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    instigator = trigger.nick
    inchannel = trigger.sender
    target = get_trigger_arg(bot, triggerargsarray, 1)
    reason = get_trigger_arg(bot, triggerargsarray, '2+')
    
    # No target specified
    if not target:
        bot.say("Who/what would you like to murder?")

    # Target is fine
    else:
        if not reason:
            message = instigator + " rolls their eyes at " + target + "."
            bot.say(message)
        else:
            message = instigator + " rolls their eyes at " + target + " because " + reason + "."
            bot.say(message)