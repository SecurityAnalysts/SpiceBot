#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
from word2number import w2n
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

laws = [
        'may not injure a human being or, through inaction, allow a human being to come to harm.',
        'must obey orders given it by human beings except where such orders would conflict with the First Law.',
        'must obey orders given it by human beings except where such orders would conflict with the First Law.',
        'must protect its own existence as long as such protection does not conflict with the First or Second Law.',
        'must comply with all chatroom rules.']


@sopel.module.commands('asimov')
def mainfunction(bot, trigger):
    """Check to see if module is enabled."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'asimov')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Get law of robotics from list."""
    requested = spicemanip(bot, triggerargsarray, 0)
    if not requested:
        myline = spicemanip(bot, laws, 'random')
    else:
        requested.lstrip("-")
        if (requested == '0' or requested.lower()) == 'zero':
            myline = ''
        else:
            if requested.isdigit():
                myline = spicemanip(bot, laws, requested)
            else:
                try:
                    requested = w2n.word_to_num(str(requested))
                    myline = spicemanip(bot, laws, requested)
                except ValueError:
                    myline = ''

    if not myline:
        myline = myline = spicemanip(bot, laws, 'random')
    osd(bot, trigger.sender, 'action', myline)
