#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import time
import datetime
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author jimender2


@sopel.module.commands('nts', 'noteToSelf')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'nts')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    command = spicemanip(bot, triggerargsarray, '1+')

    instigator = trigger.nick

    databasekey = "Notes"

    # get notes
    if not command:
        messages = get_database_value(bot, instigator, databasekey) or []
        numberOfMessages = (len(messages))
        i = 1
        while (i <= numberOfMessages):
            message = spicemanip(bot, messages, i)
            osd(bot, trigger.sender, 'say', message)
            i = i + 1
        reset_database_value(bot, instigator, databasekey)
    else:
        now = datetime.datetime.now()
        time = datetime.datetime.strftime(now, '%m/%d/%Y %H:%M:%S')
        input = time + " " + command
        adjust_database_array(bot, instigator, input, databasekey, 'add')
        osd(bot, trigger.sender, 'say', "I will remember that as best as I can")
