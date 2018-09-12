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


@sopel.module.commands('poke', 'prod')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'poke')
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
    commandused = trigger.group(1)
    for c in bot.channels:
        channel = c
    if commandused == 'prod':
        parta = "prods "
        partb = " with a big stick."
    else:
        parta = "pokes "
        partb = " with a stick."
    if not target:
        osd(bot, trigger.sender, 'say', trigger.nick + " points awkwardly at nothing.")
    elif target.startswith("bear"):
        osd(bot, trigger.sender, 'say', "Don't poke the bear.")
    elif target.lower() not in bot.privileges[channel.lower()]:
        osd(bot, trigger.sender, 'say', "I'm not sure who that is.")
    elif target == bot.nick:
        osd(bot, trigger.sender, 'say', "I am not going to poke myself for your amusement.")
    else:
        osd(bot, trigger.sender, 'action', parta + target + partb)
