#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import os
import sys
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('spicebot')
def main_command(bot, trigger):
    triggerargsarray = get_trigger_arg(bot, trigger.group(2), 'create')
    subcommand = get_trigger_arg(bot, triggerargsarray, 1)

    if not subcommand:
        osd(bot, trigger.sender, 'say', "That's my name. Don't wear it out!")
