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


@sopel.module.commands('warn')
def mainfunction(bot, trigger):
    inchannel = trigger.sender
    triggerargsarray = get_trigger_arg(bot, trigger.group(2), 'create')
    target = get_trigger_arg(bot, triggerargsarray, 2) or ''
    osd(bot, inchannel, 'action', target + "This is just a warning. Overuse of the bot, can get you kicked or banned by an operator. If you want to purely play with the bot, go to #Spicebot or #Spicebottest, or send Spicebot a PrivateMessage.")
