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

@sopel.module.commands('pints','pint')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, "pints")
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    target = get_trigger_arg(bot, triggerargsarray, 1) or "Everybody"
    if target == 'all':
        winner = "Everybody"
    elif target == trigger.nick:
        winner = "him/her-self"
    else:
        winner = target
    bot.say(trigger.nick + ' buys a pint for ' + winner)
