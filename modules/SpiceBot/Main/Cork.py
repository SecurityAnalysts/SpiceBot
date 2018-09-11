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


@sopel.module.commands('cork')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):

    target = spicemanip(bot, triggerargsarray, 1)
    isvalid, validmsg = targetcheck(bot, botcom, target, instigator)
    if isvalid == 1:
        action = "applies the Cork of Sean to " + target
    else:
        action = "applies the Cork of Sean to " + instigator.default
    osd(bot, botcom.channel_current, 'action', action)
