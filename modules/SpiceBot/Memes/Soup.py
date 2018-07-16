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


@sopel.module.commands('soup')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'soup')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)


def execute_main(bot, trigger, triggerargsarray):
    item = get_trigger_arg(bot, triggerargsarray, 0).upper() or "SOUP"
    message = "NO " + str(item) + " FOR YOU!!"
    onscreentext(bot,['say'],message)
