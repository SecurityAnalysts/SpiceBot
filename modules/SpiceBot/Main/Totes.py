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


@sopel.module.commands('totes')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    command = get_trigger_arg(bot, triggerargsarray, 1)
    if not command:
        rand = random.randint(1, 4)
        if rand == 1:
            message = "I will have a non-fat double chocolate expresso mocho soy cappachino express latte (aka crap (whatever happened to a plain cup of joe?))"
        elif rand == 2:
            message = "I want a participation medel"
        elif rand == 3:
            message = "Lifes not fair!"
        elif rand == 4:
            message = "My mommy says Im a special snowflake"
        else:
            message = "I fucked the code up real well"
    else:
        instigator = trigger.nick
        message = instigator + " thinks that " + command + " is totes obvious."
    osd(bot, trigger.sender, 'say', message)
