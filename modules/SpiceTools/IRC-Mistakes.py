#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import random
from sopel.module import OP
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('ircmistakes', 'msg', 'nick', 'attach', 'server', 'join', 'whois', 'me', 'ban', 'kick')
def execute_main(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'ircmistakes')
    osd(bot, trigger.sender, 'say', 'I believe you wanted to say ' + "/" + trigger.group(1) + " " + get_trigger_arg(bot, triggerargsarray, 0))
