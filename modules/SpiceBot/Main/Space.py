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

# author space


@sopel.module.commands('space')
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
    target = spicemanip(bot, [x for x in triggerargsarray if x in botcom.users_all], 1) or botcom.instigator
    if not target.endswith("s"):
        targetb = str(target + "s")
    else:
        targetb = str(target + "'")
    message = str("Space: the final frontier. These are the voyages of " + target + ". " + targetb + " mission: to explore strange new worlds. To seek out new life and new civilizations. To boldly go where " + target + " hasn't gone before!")
    osd(bot, trigger.sender, 'say', message)
