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


@sopel.module.commands('matrix')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'matrix')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    pill = get_trigger_arg(bot, triggerargsarray, 1)
    if not pill:
        message = 'You have two choices. redpill or bluepill'
    elif pill == 'redpill':
        message = 'You take the red pill, you stay in Wonderland, and I show you how deep the rabbit hole goes.'
    elif pill == 'bluepill':
        message = 'You take the blue pill, the story ends. You wake up in your bed and believe whatever you want to believe.'
    osd(bot, trigger.sender, 'say', message)
