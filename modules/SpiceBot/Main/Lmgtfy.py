# coding=utf-8
"""
lmgtfy.py - Sopel Let me Google that for you module
Copyright 2013, Dimitri Molenaars http://tyrope.nl/
Licensed under the Eiffel Forum License 2.
http://sopel.chat/
"""
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('lmgtfy', 'lmgify', 'gify', 'gtfy')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'lmgtfy')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Let me just... google that for you."""
    # No input
    target = get_trigger_arg(bot, triggerargsarray, 0)
    if not target:
        return osd(bot, trigger.sender, 'say', 'http://google.com/')
    osd(bot, trigger.sender, 'say', 'http://lmgtfy.com/?q=' + target.replace(' ', '+'))
