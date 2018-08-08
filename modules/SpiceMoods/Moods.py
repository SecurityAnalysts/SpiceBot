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

# author deathbybandaid


@sopel.module.commands('mood')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):

    validmoodcommands = ['check', 'change', 'set']
    moodcommand = get_trigger_arg(bot, [x for x in triggerargsarray if x in validmoodcommands], 1) or 'check'
    if moodcommand in triggerargsarray:
        triggerargsarray.remove(moodcommand)
    moodcommand = moodcommand.lower()

    currentmood = get_database_value(bot, botcom.channel_current, 'mood') or 'happy'

    if moodcommand == 'check':
        osd(bot, trigger.sender, 'say', botcom.channel_current + " is currently in a " + currentmood + ".")
        return

    if moodcommand in ['change', 'set']:
        moodset = get_trigger_arg(bot, triggerargsarray, 0) or 0
        if not moodset:
            osd(bot, trigger.sender, 'say', "What mood is " + botcom.channel_current + " in?")
            return
        moodset = moodset.lower()
        osd(bot, trigger.sender, 'say', botcom.channel_current + " has changed from " + currentmood + " to " + moodset + ".")
        set_database_value(bot, botcom.channel_current, 'mood', moodset)
        return
