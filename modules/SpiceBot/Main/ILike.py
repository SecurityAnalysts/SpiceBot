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


@sopel.module.commands('like')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'like')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    instigator = trigger.nick
    target = spicemanip(bot, triggerargsarray, 1)
    command = spicemanip(bot, triggerargsarray, '1+')
    if not command:
        rand = random.randint(1, 10)
        if rand == 3:
            osd(bot, trigger.sender, 'say', "I like porn")
        else:
            osd(bot, trigger.sender, 'say', "I like turtles")
    elif command == "trains":
        osd(bot, trigger.sender, 'say', "I like trains.")

    else:
        message = "I like " + command + "."
        osd(bot, trigger.sender, 'say', message)
