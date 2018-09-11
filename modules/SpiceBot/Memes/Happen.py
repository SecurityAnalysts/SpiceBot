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


@sopel.module.commands('happen')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'happen')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    happen = get_trigger_arg(bot, triggerargsarray, 0)
    if not happen:
        message = "Stop trying to make stuff happen. It's not going to happen"
    else:
        message = "Stop trying to make " + str(happen) + " happen. It's not going to happen"
    osd(bot, trigger.sender, 'say', message)
