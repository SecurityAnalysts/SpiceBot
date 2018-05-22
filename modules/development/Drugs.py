#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('drugs')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):

    locationorperson = get_trigger_arg(bot,triggerargsarray,1)
    person = get_trigger_arg(bot,triggerargsarray,1) or trigger.nick
    druglocation = get_trigger_arg(bot,triggerargsarray,'1+') or "somewhere tropical"
    drugdisplay = "to " + druglocation
    displaymsg = "Whoops, something went wrong. Not sure how that got fucked up."

    # Nothing special
    if not locationorperson:
        displaymsg = person + " contemplates selling everything and moving " + drugdisplay + " to sell drugs on a beach."

    # Someone specified
    elif locationorperson.lower() in [u.lower() for u in bot.users]:
        druglocation = get_trigger_arg(bot,triggerargsarray,'2+') or "somewhere tropical"
        displaymsg = person + " should really consider selling everything and moving " + drugdisplay + " to sell drugs on a beach."

    # Location specified
    elif locationorperson.lower() not in [u.lower() for u in bot.users]:
        person = trigger.nick
        displaymsg = person + " contemplates selling everything and moving " + drugdisplay + " to sell drugs on a beach."

    # Error encountered, nothing worked
    else:
        displaymsg = "I appear to have some fucked up code rules going on. Someone fix this shit."
        
    bot.say(displaymsg)
