#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import os
import sopel.module
import sys
import time
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('butts', 'butt')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'butts')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    target = spicemanip(bot, triggerargsarray, 1)
    instigator = trigger.nick
    if not target:
        action = "rains butts down on everyone."
    elif target == instigator:
        action = "kicks " + instigator + " in the butt."
    else:
        action = "rains butts down on " + target
    osd(bot, botcom.channel_current, 'action', action)
