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


@sopel.module.commands('oprah')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'oprah')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    item = spicemanip(bot, triggerargsarray, 0)
    if not item:
        item = "a car"
    else:
        if item.startswith('a') or item.startswith('e') or item.startswith('i') or item.startswith('o') or item.startswith('u'):
            item = str('an ' + item)
        else:
            item = str('a ' + item)
    message = "You get " + item + "! And You get " + item + "! Everyone gets " + item + "!"
    osd(bot, trigger.sender, 'say', message)
