#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
# import sopel.module
from sopel.module import commands, nickname_commands, rule, priority, example
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@nickname_commands('who')
@commands('who')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'who')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    funlist = [
                "Who put the bomp in the bomp bah bomp bah bomp",
                "Who put the ram in the rama lama ding dong",
                "Who put the bop in the bop shoo bop shoo bop",
                "Who put the dip in the dip da dip da dip"]
    message = get_trigger_arg(bot, funlist, 'random')
    osd(bot, trigger.sender, 'say', message)
