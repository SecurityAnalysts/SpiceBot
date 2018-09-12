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


@sopel.module.commands('congratz')
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
    rand = random.randint(1, 4)
    if rand == 1:
        osd(bot, trigger.sender, 'say', "                       (")
        osd(bot, trigger.sender, 'say', "      __________       )\\")
        osd(bot, trigger.sender, 'say', "     /         /\______{,}")
        osd(bot, trigger.sender, 'say', "     \_________\/")
    else:
        osd(bot, trigger.sender, 'say', "https://media1.tenor.com/images/25f11267d63bc6a6193e3fb69cbc2857/tenor.gif?itemid=7323300")
