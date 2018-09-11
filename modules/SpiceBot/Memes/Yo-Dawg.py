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


@sopel.module.commands('yodawg')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'yodawg')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    target = spicemanip(bot, triggerargsarray, '1+')
    if target:
        message = "Yo Dawg! I heard you liked " + target + ", So I put a " + target + " in/on your " + target + "!!!"
    else:
        message = "I'm not sure who or what the hell that is."
    osd(bot, trigger.sender, 'say', message)
