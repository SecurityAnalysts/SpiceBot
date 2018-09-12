#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
from random import randint
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('tap', 'mic')
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
    instigator = trigger.nick
    target = spicemanip(bot, triggerargsarray, 1)
    if not target:
        decide = randint(1, 5)
        if decide == 4:
            osd(bot, trigger.sender, 'say', "For Fucks Sake " + instigator + ", of course it's bloody well on!")
        elif decide == 5:
            osd(bot, trigger.sender, 'action', "clocks " + instigator + " around the head with a mic stand.")
            osd(bot, trigger.sender, 'say', instigator + ", if you do that again you'll be eating a speaker.")
        else:
            osd(bot, trigger.sender, 'say', "*Tap, Tap* ...is this thing on?")
    else:
        osd(bot, trigger.sender, 'say', "Hey " + target + ",,,, you there?")
