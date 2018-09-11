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


@sopel.module.commands('kids')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'kids')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    target = spicemanip(bot, triggerargsarray, 1)
    isValid = targetcheck(bot, botcom, target, instigator)
    if not target:
        target = trigger.nick
        message  = "Is that what the kids are calling it these days, " + target
    elif isValid == 1:
        message  = "Is that what the kids are calling it these days, " + target
    else:
        something = spicemanip(bot, triggerargsarray, '1+')
        if something.endswith('s'):
            message = something + "??? is THAT what the kids are calling them these days?"
        else:
            message = something + "??? is THAT what the kids are calling it these days?"
    osd(bot, trigger.sender, 'say', message)
