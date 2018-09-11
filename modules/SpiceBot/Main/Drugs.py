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


@sopel.module.commands('drugs')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):

    locationorperson = spicemanip(bot, triggerargsarray, 1)
    person = spicemanip(bot, triggerargsarray, 1) or trigger.nick
    druglocation = spicemanip(bot, triggerargsarray, '1+') or "somewhere tropical"
    drugdisplay = "to " + druglocation
    displaymsg = "Whoops, something went wrong. Not sure how that got fucked up."

    # Nothing specified
    if not locationorperson:
        displaymsg = person + " contemplates selling everything and moving " + drugdisplay + " to sell drugs on a beach."

    # Something specified
    elif locationorperson:
        # input is person
        if locationorperson.lower() in [u.lower() for u in bot.users]:
            druglocation = spicemanip(bot, triggerargsarray, '2+') or "somewhere tropical"
            drugdisplay = "to " + druglocation
            displaymsg = person + " should really consider selling everything and moving " + drugdisplay + " to sell drugs on a beach."

        # input is location
        else:
            person = trigger.nick
            displaymsg = person + " contemplates selling everything and moving " + drugdisplay + " to sell drugs on a beach."

    # Error encountered, nothing worked
    else:
        displaymsg = "I appear to have some fucked up code rules going on. Someone fix this shit."

    osd(bot, trigger.sender, 'say', displaymsg)
