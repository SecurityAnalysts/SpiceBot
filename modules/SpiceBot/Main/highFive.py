#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import random
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author jimender2


@sopel.module.commands('hf', 'highfive', 'high-five', 'highfives')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'hf')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    failureodds = 4
    target = spicemanip(bot, triggerargsarray, 1)
    backfires = [
                " drops everything they are doing and goes to high five " + target + ", but they miss.",
                " overestimated their capabilities and knocks themselves out.",
                " goes and trips before they can manage to high five " + target + ".",
                " high-fives " + target + " too enthusiastically and breaks their hand."]

    if not target:
        osd(bot, trigger.sender, 'say', trigger.nick + ' high fives everyone!')
    elif target == 'group':
        osd(bot, trigger.sender, 'say', trigger.nick + ', high fives everyone all at once.')
    elif target == 'all' or target == 'everyone' or target == 'everyones':
        osd(bot, trigger.sender, 'say', trigger.nick + " high fives, one at a time!")
    elif target != bot.nick:
        failchance = random.randint(1, failureodds)
        if failchance == 1:
            hffail = spicemanip(bot, backfires, 'random')
            osd(bot, trigger.sender, 'say', trigger.nick + hffail)
        else:
            osd(bot, trigger.sender, 'say', trigger.nick + " high fives %s, maintaining eye contact the entire time!" % target)
