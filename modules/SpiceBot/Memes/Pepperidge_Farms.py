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


@sopel.module.commands('pf')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'pf')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    pfremembers = get_trigger_arg(bot, triggerargsarray, 0)
    if pfremembers:
        message = "Pepperidge Farms remembers " + str(pfremembers)
    else:
        message = "You're so old Pepperidge Farms doesn't even remember that."
    osd(bot, trigger.sender, 'say', message)
