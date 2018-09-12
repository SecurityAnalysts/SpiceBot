#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import os
import sys
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

defaultoptions = [
    "Have you tried turning it off and on again?", "Four! I mean five! I mean FIRE!", "Have you tried clicking on it repeatedly?", "No, 'any' key means push any key you like. There is no specific'any' key.",
    "Let me just remote in and... yes, that's me moving your mouse. No, I'm not a virus. You know who I am. You've met me. Oh for... stop moving the mouse while I'm fixing things!",
    "Oh, you've Googled the issue yourself and tried to fix it yourself before lodging a ticket? Thanks for that.", "Have you tried chewing the cable?", "Instructions unclear, dick stuck in ceiling fan.",
    "YOU MUST CONSTRUCT ADDITIONAL PYLONS!", "Have you tried flinging feces at it?", "Did you try licking the mouse? Double-lick?", "Did you try replacing all the ones with zeros?", "Try cooling it with a jug of water.",
    "Error: Keyboard not detected. Press 'F1' to continue.",
]


@sopel.module.commands('techsupport', 'itsupport')
def mainfunction(bot, trigger):
    """Check that the module is enabled."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'techsupport')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Retrieve an entry from the database."""
    databasekey = 'techsupport'
    command = spicemanip(bot, triggerargsarray, 1) or 'get'
    if not sayingscheck(bot, databasekey) and command != "add":
        sayingsmodule(bot, databasekey, defaultoptions, 'initialise')
    message = sayingsmodule(bot, databasekey, triggerargsarray, command)
    osd(bot, trigger.sender, 'say', message)
