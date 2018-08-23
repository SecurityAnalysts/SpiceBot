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


@sopel.module.commands('poop', 'poops', 'shit', 'shits')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'poop')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    failureodds = 4
    if bot.nick.endswith('dev'):
        failureodds = 2
    target = get_trigger_arg(bot, triggerargsarray, 1)
    backfires = [" drops their pants and squats on " + target + "'s desk, but all they manage to do is fart.",
                 " overestimated their capabilities and poops themselves.",
                 " gets halfway through pooping before realising that this is their own desk, not " + target + "'s.",
                 " trips over taking their pants off and shits everywhere BUT the desk."]

    if not target:
        versionblank = get_trigger_arg(bot, ['corner', 'boss'], 'random')
        if versionblank == 'corner':
            osd(bot, trigger.sender, 'say', trigger.nick + ' poops in the designated corner!')
        elif versionblank == 'boss':
            osd(bot, trigger.sender, 'say', "Boss makes a dollar, I make a dime. That's why I poop on company time.")
    elif target == 'group':
        target = get_trigger_arg(bot, triggerargsarray, 2) or trigger.nick
        osd(bot, trigger.sender, 'say', target + ', get your poop in a group.')
    elif target == 'all' or target == 'everyone' or target == 'everyones':
        osd(bot, trigger.sender, 'say', trigger.nick + " poops on everyone's desk, one at a time!")
    elif target != bot.nick:
        failchance = random.randint(1, failureodds)
        if failchance == 1:
            poopfail = get_trigger_arg(bot, backfires, 'random')
            osd(bot, trigger.sender, 'say', trigger.nick + poopfail)
        else:
            osd(bot, trigger.sender, 'say', trigger.nick + ' poops on ' + target + "'s desk, maintaining eye contact the entire time!")
