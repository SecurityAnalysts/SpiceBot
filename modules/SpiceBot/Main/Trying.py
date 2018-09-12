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


@sopel.module.commands('trying')
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
    target = spicemanip(bot, triggerargsarray, 1)
    phrase = spicemanip(bot, triggerargsarray, '1+')
    action = spicemanip(bot, triggerargsarray, '2+')
    if target:
        if target == 'to':
            parta = phrase
            partb = action
        else:
            parta = str("to " + phrase)
            partb = phrase
        statement = str("Are you trying " + parta + "? 'Cuz that's how you " + partb + "!!!")
        osd(bot, trigger.sender, 'say', statement)
    else:
        osd(bot, trigger.sender, 'say', "I haven't got the faintest idea what you are trying to do.")
