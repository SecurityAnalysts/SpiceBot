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


@sopel.module.commands('gong')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'gong')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    person = get_trigger_arg(bot, triggerargsarray, 1)

    if person == bot.nick:
        message = "Spicebot grabs " + trigger.nick + " with a hook and drags them out of the room because they tried to gong Spicebot."
    else:
        message = "Spicebot grabs " + person + " with a hook and drags them out of the room."

    osd(bot, trigger.sender, 'say', message)
