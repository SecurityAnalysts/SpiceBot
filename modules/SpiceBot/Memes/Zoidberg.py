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


@sopel.module.commands('zoidberg')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'zoidberg')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    string = spicemanip(bot, triggerargsarray, 0)
    instigator = trigger.nick
    if string:
        if string.startswith("your ") or string.startswith("ur "):
            string = spicemanip(bot, triggerargsarray, '2+')
        if string.endswith("s"):
            message = "Your " + str(string) + " are bad, and you should feel bad!"
        else:
            message = "Your " + str(string) + " is bad, and you should feel bad!"
    else:
        message = "Hey " + instigator + ": your face is bad and you should feel bad!"
    osd(bot, trigger.sender, 'say', message)
