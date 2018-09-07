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


@sopel.module.commands('guns', 'gun')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'guns')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    target = get_trigger_arg(bot, triggerargsarray, 1) or trigger.nick
    if not target:
        action = ["Guns don't kill people.", "People kill people.", "With Guns."]
    else:
        action = ["Guns don't kill people.", target + " kills people.", "With Guns."]
    osd(bot, botcom.channel_current, 'action', action)
