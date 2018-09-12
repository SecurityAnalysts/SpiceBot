#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
from datetime import datetime
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('sysadmin', 'sysadminday')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'sysadmin')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    today = datetime.datetime.now()
    sysadminday = datetime.datetime.strptime('Jul 27 2018', '%b %d %Y')
    if sysadminday > today:
        daystillsysadminday = sysadminday - today
        message = "There are " + str(daystillsysadminday.days) + " days till SysAdmin day"
    elif sysadminday < today:
        daystillsysadminday = sysadminday - today
        message = "SysAdmin day happened " + str(daystillsysadminday.days) + " ago."
    else:
        message = "Happy Sysadmin day"
    osd(bot, trigger.sender, 'say', message)
