#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

fishtypes = ["Pike","Carp","Marlin","Trout","Cod","Anchovy","Venezuelan Beaverfish","fish","jellyfish"]
vowels = ('a','e','i','o','u','A','E','I','O','U')

@sopel.module.commands('fish')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    target = get_trigger_arg(bot, triggerargsarray, 1)
    reason = get_trigger_arg(bot, triggerargsarray, '2+')
    message = "Whoops, something went wrong."
    fishtype = get_trigger_arg(bot,fishtypes,'random')
    fishmsg = "a " + fishtype
    # Vowel awareness
    if fishtype.startswith(vowels):
        fishmsg = "an " + fishtype

    # No target specified
    if not target:
        message = "You haven't told me who or what you want to slap, you moron."

    # Can't slap the bot
    if target == bot.nick:
        message = "Get fucked, that's not gonna happen."

    # Target is bear
    elif target.startswith("bear"):
        if not reason:
            message = trigger.nick + " feeds " + target + " a tasty " + fishtype + "."
        else:
            if reason.startswith('for ') or reason.startswith('because ') or reason.startswith('cause '):
                message = trigger.nick + " feeds " + target + " a tasty " + fishtype + " " + reason + "."
            else:
                message = trigger.nick + " feeds " + target + " a tasty " + fishtype + " for " + reason + "."

    # Target is fine
    else:
        if not reason:
            message = trigger.nick + " slaps " + target + " with " + fishmsg + "."
        else:
            if reason.startswith('for ') or reason.startswith('because ') or reason.startswith('cause '):
                message = trigger.nick + " slaps " + target + " with " + fishmsg + " " + reason + "."
            else:
                message = trigger.nick + " slaps " + target + " with " + fishmsg + " for " + reason + "."

    bot.say(message)
