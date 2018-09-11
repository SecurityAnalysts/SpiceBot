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


@sopel.module.commands('hb')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'hb')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    hashstring = get_trigger_arg(bot, triggerargsarray, '1+') or 'fail'
    if hashstring == "fwp":
        hashstring = "firstworldproblems"
    if hashstring == "ym":
        hashstring = "yo momma"
    response = "hashbrown " + str(hashstring)
    osd(bot, trigger.sender, 'say', response)
