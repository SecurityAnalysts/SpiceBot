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


@sopel.module.commands('airbiscuit', 'float')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'airbiscuit')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    target = spicemanip(bot, triggerargsarray, 1)
    message = ""
    isvalid, validmsg = targetcheck(bot, botcom, target, instigator)
    if not target:
        message = trigger.nick + " floats an air biscuit."
    elif isvalid == 0:
        message = "I'm not sure who that is."
    elif isvalid == 3:
        message = "Well, that was truly disgusting!"
    else:
        message = trigger.nick + " floats an air biscuit in the general direction of " + target + "."
    osd(bot, trigger.sender, 'say', message)
