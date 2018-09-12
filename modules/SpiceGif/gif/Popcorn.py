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
gifshareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(gifshareddir)
from GifShared import *

# author jimender2

weapontypes = ["Axe", "Sword", "Revolver"]
commandarray = ["add", "remove", "count", "last"]


@sopel.module.commands('popcorn', 'pc')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'popcorn')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    target = spicemanip(bot, triggerargsarray, 1)
    if not target:
        osd(bot, trigger.sender, 'action', "grabs popcorn and goes to watch the action")
        osd(bot, trigger.sender, 'say', "https://media2.giphy.com/media/daJWXqaZFqh0s/giphy.gif")
        osd(bot, trigger.sender, 'action', "munch, munch")
    else:
        osd(bot, trigger.sender, 'action', "grabs popcorn and goes to watch " + target + "'s situation unfold.")
