#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import random
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

replies = ["Honey, how do I change a diaper?", "If you put it on the to-do list, I told you I'll do it. You don't have to remind me about it every 6 months.", "*Buuuurp*", "Sure honey, that's fine.", "*Sigh* Yes dear."]
actions = ["burps", "scratches his ass", "farts", "opens a beer"]


@sopel.module.commands('husband')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    decide = random.randint(1, 10)
    if decide > 7:
        response = spicemanip(bot, actions, 'random')
        osd(bot, trigger.sender, 'action', response)
    else:
        answer = spicemanip(bot, replies, 'random')
        osd(bot, trigger.sender, 'say', answer)
