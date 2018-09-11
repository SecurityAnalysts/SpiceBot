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


@sopel.module.commands('thug')
def mainfunction(bot, trigger):
    """Check if module is enabled."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'thug')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Handle the main task itself."""
    target = spicemanip(bot, triggerargsarray, 1)
    isvalid, validmsg = targetcheck(bot, botcom, target, instigator)
    message = "%s didn't choose the thug life, the thug life chose %s." % (instigator.default, instigator.default)
    if not isvalid == 0:
        message = "%s didn't choose the %s life, the %s life chose %s." % (instigator.default, target, target, instigator.default)
    osd(bot, trigger.sender, 'say', message)
