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

# author jimender2


@sopel.module.commands('serenity')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'serenity')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    osd(bot, trigger.sender, 'say', "Lando grant me the serenity")
    osd(bot, trigger.sender, 'say', "to accept the things I cannot change")
    osd(bot, trigger.sender, 'say', "courage to change the things I can")
    osd(bot, trigger.sender, 'say', "and wisdom to know the difference.")
