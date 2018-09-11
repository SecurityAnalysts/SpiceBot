#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sopel
from sopel import module, tools
import random
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('dbshow')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    nick = spicemanip(triggerargsarray, 0)
    osd(bot, trigger.sender, 'say', "nick: " + nick)
    dbkey = spicemanip(triggerargsarray, 1)
    osd(bot, trigger.sender, 'say', "dbkey: " + dbkey)
    # dbresult = get_database_value(bot,
    # get_database_value(bot, nick, databasekey):
