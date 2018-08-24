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


# @sopel.module.commands('dbbtest')
# def mainfunction(bot, trigger):
#    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
#    execute_main(bot, trigger, triggerargsarray, botcom, instigator)

@sopel.module.commands('dbbtest')
def execute_main(bot, trigger):
    osd(bot, trigger.sender, 'say', "This is deathbybandaid's test module")

    thisdict = dict(apple="green", banana="yellow", cherry="red")

    bot.say(str(thisdict["apple"]))

    botdict = get_database_dict(bot, bot.nick, 'dicttest')

    bot.say(str(botdict))
