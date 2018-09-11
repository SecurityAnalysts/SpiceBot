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


@sopel.module.commands('onetozero','120')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'onetozero')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    current_translate = spicemanip(bot, triggerargsarray, 0) or 0
    if not str(current_translate).isdigit():
        osd(bot, trigger.sender, 'say', "Sorry. What you input is not binary")

    else:
        message = current_translate.replace('0', '1')
        osd(bot, trigger.sender, 'say', message)
