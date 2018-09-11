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


@sopel.module.commands('myown')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'myown')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    myown = spicemanip(bot, triggerargsarray, 0)
    message = "Fine! I'll start my own my casino with blackjack and hookers!"
    if myown and bot.nick not in myown:
        message = "Fine! I'll start my own " + myown + ", with blackjack and hookers!"
    osd(bot, trigger.sender, 'say', message)
