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

weapontypes = ["Axe", "Sword", "Revolver"]
commandarray = ["add", "remove", "count", "last"]


@sopel.module.commands('popcorn', 'pc')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'popcorn')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    target = get_trigger_arg(bot, triggerargsarray, 1)
    if not target:
        osd(bot, trigger.sender, 'action', "grabs popcorn and goes to watch the action")
        osd(bot, trigger.sender, 'say', "https://media2.giphy.com/media/daJWXqaZFqh0s/giphy.gif")
        osd(bot, trigger.sender, 'action', "munch, munch")
    else:
        osd(bot, trigger.sender, 'action', "grabs popcorn and goes to watch " + target + "'s situation unfold.")
