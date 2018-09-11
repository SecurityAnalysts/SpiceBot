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
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    command = get_trigger_arg(bot, triggerargsarray, '1+')

    instigator = trigger.nick

    databasekey = "Notes"

    # get notes
    if not command:
        messages = get_database_value(bot, instigator, databasekey) or []
        numberOfMessages = (len(messages))
        i = 1
        while (i <= numberOfMessages):
            message = get_trigger_arg(bot, messages, i)
            osd(bot, trigger.sender, 'say', message)
            i = i + 1
        reset_database_value(bot, instigator, databasekey)
    else:
        now = datetime.datetime.now()
        time = datetime.datetime.strftime(now, '%m/%d/%Y %H:%M:%S')
        input = time + " " + command
        adjust_database_array(bot, instigator, input, databasekey, 'add')
        osd(bot, trigger.sender, 'say', "I will remember that as best as I can")
