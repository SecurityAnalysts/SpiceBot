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

# author SniperClif


@sopel.module.commands('payme')
def mainfunction(bot, trigger):
    """Check to see if module is enabled."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Take input and use it in a "fuck you, pay me" style sentence."""
    target = get_trigger_arg(bot, triggerargsarray, '1+')
    if not target:
        osd(bot, trigger.sender, 'say', "Like I always say, 'Fuck you, pay me!'")
    else:
        osd(bot, trigger.sender, 'say', target.upper() + ", fuck you, pay me! ")
