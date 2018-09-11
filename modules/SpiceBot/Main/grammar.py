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

responselist = ["KILL THE GRAMMAR NAZI!",
                "Grammar fucker, do you understand it?",
                "Eats, Shoots and Leaves or Eats Shoots and Leaves?"]


@sopel.module.commands('grammar')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'grammar')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    displaymsg = spicemanip(bot, responselist, 'random')
    osd(bot, trigger.sender, 'say', displaymsg)
