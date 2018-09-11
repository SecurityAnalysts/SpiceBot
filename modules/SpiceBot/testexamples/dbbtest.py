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

import textwrap
import collections
import json

import requests

from sopel.logger import get_logger
from sopel.module import commands, rule, example, priority

sys.setdefaultencoding('utf-8')


@sopel.module.commands('dbbtest')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    osd(bot, trigger.sender, 'say', "This is deathbybandaid's test module")

    testsgood = [
                    0, 1, 2, 3, 4, 5, 6, 7,
                    "'reverse'", "'count'", "'dedupe'", "'sort'",
                    "'lower'", "'upper'", "'title'",
                    "'list'", "'andlist'", "'orlist'", "'last'", "'random'"
                    ]
    triggerargstest = [
                        8, 9,
                        "'2^6'", "'4!'", "'4+'", "'4-'", "'4<'", "'4>'"
                        ]
    argtypetest = ["spicemanip_old", "spicemanip"]

    for tasktest in triggerargstest:

        bot.say("                    Testing " + str(tasktest))

        for testtype in argtypetest:

            testevalstr = str(str(testtype) + "(bot, trigger.group(2), " + str(tasktest) + ")")
            try:
                testeval = eval(testevalstr)
            except NameError:
                testeval = "N/A"

            if testtype == "spicemanip":
                testtype = str("      " + testtype)
            bot.say(str(testtype) + "     " + str(testeval))
