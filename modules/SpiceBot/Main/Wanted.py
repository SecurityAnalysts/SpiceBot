#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from random import random
from random import randint
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('wanted')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    target = spicemanip(bot, triggerargsarray, 1)
    for c in bot.channels:
        channel = c
    if not target:
        osd(bot, trigger.sender, 'say', 'You must choose a Person.')
    elif target.lower() not in bot.privileges[channel.lower()]:
        osd(bot, trigger.sender, 'say', "I'm not sure who that is.")
    elif target == bot.nick:
        osd(bot, trigger.sender, 'say', "Well, thanks for thinking of me!")
    else:
        rando = randint(0, 50)
        if rando == 0:
            osd(bot, trigger.sender, 'say', target + " was never wanted as a child, and still isn't wanted!")
        else:
            osd(bot, trigger.sender, 'say', target + ' was never wanted as a child, but now is wanted in ' + str(rando) + ' states!')
