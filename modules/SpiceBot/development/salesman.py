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

# author deathbybandaid


@sopel.module.commands('salesman')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    thing = get_trigger_arg(bot, triggerargsarray, 1) or 'car'
    therest = get_trigger_arg(bot, triggerargsarray, "2+") or 'spaghetti'
    osd(bot, trigger.sender, 'action', "slaps roof of " + thing)
    osd(bot, trigger.sender, 'say', "this bad boy can fit so much fucking " + therest + " in it")
