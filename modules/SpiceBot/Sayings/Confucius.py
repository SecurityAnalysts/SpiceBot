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

# author = dysonparkes
defaultoptions = [
    "Man who lie on back, fucks up.", "Man who piss into wind get wet.", "Panties not best thing on earth, but next to it.", "Virginity like bubble: one prick, all gone.", "Man who stand on toilet high on pot.",
    "Man who stand on toilet high on pot.", "If a bulldog and a Shitsu are mated, it would be called a Bullshit.", "Nail on board is not good as screw on bench.",
    "Tight dress is like a barbed fence; it protects the premises without restricting the view."
]


@sopel.module.commands('confucius')
def mainfunction(bot, trigger):
    """Check to see if module is enabled."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'yes')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Retrieve 'Confucius' saying from database."""
    databasekey = 'confucius'
    command = spicemanip(bot, triggerargsarray, 1) or 'get'
    if not sayingscheck(bot, databasekey) and command != "add":
        sayingsmodule(bot, databasekey, defaultoptions, 'initialise')
    message = sayingsmodule(bot, databasekey, triggerargsarray, command)
    if not message.startswith("Confucius"):
        message = "Confucius say... " + message
    osd(bot, trigger.sender, 'say', message)
