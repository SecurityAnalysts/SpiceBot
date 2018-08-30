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

# author jimender2

insalton = ["clock speed",
            "test"]

insalttw = ["clock speed",
            "test"]

insaltth = ["clock speed",
            "test"]


@sopel.module.commands('insult')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'insult')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    answer = get_trigger_arg(bot, insalton, 'random')
    answer = get_trigger_arg(bot, insalttw, 'random')
    answer = get_trigger_arg(bot, insaltth, 'random')

    osd(bot, trigger.sender, 'say', "do the thing")
