#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from random import randint
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('ride')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    diceroll = randint(0, 6)
    if diceroll == 3:
        osd(bot, trigger.sender, 'say', "Slow ride https://www.youtube.com/watch?v=T4287tw_dwk")
    else:
        instigator = trigger.nick
        target = spicemanip(bot, triggerargsarray, 1) or instigator
        if target == instigator:
            message = target + " wants to put on some mad max gear, drop acid, and ride a motorcycle through the desert, while listening to some CoC."
        else:
            message = target + " should put on some mad max gear, drop acid, and ride a motorcycle through the desert, while listening to some CoC."
        osd(bot, trigger.sender, 'say', message)
