#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import os
import sopel.module
import sys
import time
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('apu')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'apu')
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
    if decide == 1:
        message = "Who needs the Kwik-E-Mart? I do..."
        osd(bot, trigger.sender, 'say', message)
        time.sleep(2)
        actions = "starts crying"
        osd(bot, trigger.sender, 'action', actions)
    else:
        message = "Thank you, come again."
        osd(bot, trigger.sender, 'say', message)
